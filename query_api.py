import re
import os
import click
import subprocess
import api_parsing
from pygments.token import Name
from pygments.lexers import CLexer, CppLexer

API_CALLS = []

def get_c_cpp_files(root_dir):
    """
    Retrieve a list of C and C++ files from the specified root directory.

    Args:
        root_dir (str): The root directory to search for C and C++ files.

    Returns:
        list: A list of file paths for C and C++ files found in the root directory.
    """
    c_files = []
    cpp_files = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".c"):
                c_files.append(os.path.join(dirpath, filename))
            elif filename.endswith(".cpp"):
                cpp_files.append(os.path.join(dirpath, filename))
    
    return c_files if c_files else cpp_files


def extract_functions_from_code(code, language):
    """
    Extracts functions from the given code based on the specified language.

    Args:
        code (str): The code from which to extract functions.
        language (str): The programming language of the code ("C++" or "C").

    Returns:
        list: A list of unique function names extracted from the code.
    """
    lexer = CppLexer() if language == "C++" else CLexer()
    tokens = lexer.get_tokens(code)
    functions = [tok[1] for tok in tokens if tok[0] in Name]
    functions_1 = [tok[1] for tok in tokens if tok[0] == Name.Function]
    return list(set(functions).union(set(functions_1)))


def remove_items(test_list, items):
    """
    Remove specified items from a list.

    Args:
        test_list (list): The list from which items will be removed.
        items (list): The items to be removed from the list.

    Returns:
        list: A new list with the specified items removed.
    """
    res = list(filter((items).__ne__, test_list))
    return res

def get_false_pos() -> list():
    """
    Retrieves false positive matches from the output file.

    Returns:
        A list of false positive matches.
    """
    command = r"grep -Pzo '\^\^ \w+\nSymbol Definitions:\n\nSymbol References:\n\nDocumented in:\n' /home/nos1abt/py-test/output.txt"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    f_pos = output.decode()
    if error:
        print(f"Error: {error}")
    else:
        pattern = r"\^\^ (\w+)"
        matches = re.findall(pattern, f_pos)
        # pprint.pprint(matches) # for debugging purposes
        return matches




# def API_Calls_fetch(repo_path, version):
#     """
#     Fetches API calls and macros from C/C++ files in the given repository path.

#     Args:
#         repo_path (str): The path to the repository.
#         version (str): The version of the API.".

#     Returns:
#         None
#     """
#     MACROS = []
#     functions = []
#     language = ""
#     macro_pattern = re.compile(r"#define\s+(\w+)")

#     for file in get_c_cpp_files(repo_path):
#         fdata = open(file, "r").read()
#         language = "C" if file.endswith(".c") else "C++"
#         matches = macro_pattern.findall(fdata)
#         MACROS.extend(matches)
#         functions.extend(extract_functions_from_code(fdata, language))

#     MACROS = set(MACROS)
#     functions = set(functions)
#     with open("output.txt", "w") as file:
#         for item in functions:
#             if item not in MACROS:
#                 command = f"echo ^^ {item} ; /home/bsp_projects/elixir/query.py {version} ident {item} C ;  echo \n"
#                 subprocess.run(command, shell=True, stdout=file)

def API_Calls_fetch(repo_path, version):
    """
    Fetches API calls and macros from C/C++ files in the given repository path.

    Args:
        repo_path (str): The path to the repository.
        version (str): The version of the API.

    Returns:
        None
    """
    MACROS = []
    functions = []
    language = ""
    macro_pattern = re.compile(r"#define\s+(\w+)")

    with click.progressbar(get_c_cpp_files(repo_path), label="Processing files") as bar:
        for file in bar:
            fdata = open(file, "r").read()
            language = "C" if file.endswith(".c") else "C++"
            matches = macro_pattern.findall(fdata)
            MACROS.extend(matches)
            functions.extend(extract_functions_from_code(fdata, language))

    MACROS = set(MACROS)
    functions = set(functions)
    with open("output.txt", "w") as file:
        with click.progressbar(functions, label="Runnning Queries! - be patient!") as bar:
            for item in bar:
                if item not in MACROS:
                    command = f"echo ^^ {item} ; /home/bsp_projects/elixir/query.py {version} ident {item} C ;  echo \n"
                    subprocess.run(command, shell=True, stdout=file)


def main(path_api_output, repo_output_folder, repo_path, version):
    """
    Main function to run API_Calls_hunter and process the output.

    Args:
        path_api_output (str): Path to the API output file.
        repo_output_folder (str): Path to the output folder for the repository.
        repo_path (str): Path to the repository.

    Returns:
        None
    """
    print(path_api_output, repo_output_folder)

    # with click.progressbar(length=1, label="Running API_Calls_hunter") as bar:
    #     API_Calls_fetch(repo_path, version)
    #     bar.update(1)
    API_Calls_fetch(repo_path, version)
    get_false_pos()
    api_parsing.replace_lines_in_file("output.txt", path_api_output, repo_output_folder)
    l = api_parsing.extract_words_and_types(path_api_output, repo_output_folder)
    api_parsing.filer_final_api_calls(repo_output_folder, "function", l)
    l.clear()
    os.system("rm output.txt")


