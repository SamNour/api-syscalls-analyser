import utilities
import query_api
import os
import re


# $ ./query.py v4.10 ident raw_spin_unlock_irq C
# $ ./query.py v4.10 file /kernel/sched/clock.c
def remove_pattern_from_list(lst) -> list():
    """
    Removes specific patterns and false positives from a list.

    Args:
        lst (list): The input list.

    Returns:
        list: The modified list with patterns and false positives removed.
    """
    i = 0
    FP = query_api.get_false_pos()
    for index, _ in enumerate(FP):
        FP[index] = f"^^ {FP[index]}\n"

    while i < len(lst) - 1:
        if (
            lst[i] == "Symbol References:\n"
            and lst[i + 1] == "\n"
            or lst[i] == "Symbol Definitions:\n"
            and lst[i + 1] == "\n"
            or lst[i] == "Documented in:\n"
            and lst[i + 1] == "\n"
        ):
            del lst[i : i + 2]
        elif lst[i] in FP:
            del lst[i : i + 1]
        else:
            i += 1
    return lst


def replace_lines_in_file(filename, path_api_output, repo_output_folder):
    """
    Replaces lines in a file with the contents of another file.

    Args:
        filename (str): The path to the file whose lines need to be replaced.
        path_api_output (str): The path to the file containing the new lines.
        repo_output_folder (str): The path to the folder where the modified file will be moved.

    Returns:
        None
    """
    with open(filename, "r") as file:
        lines = file.readlines()
        remove_pattern_from_list(lines)
    with open(path_api_output, "w") as file:
        file.writelines(lines)
    os.system(f"mv {path_api_output} {repo_output_folder}")


def extract_words_and_types(repo_output_folder, path_api_output):
    """
    Extracts words and their corresponding types from a file and saves the result in a text file.

    Args:
        repo_output_folder (str): The path to the repository output folder.
        path_api_output (str): The path to the API output file.

    Returns:
        list: A list of tuples containing the extracted word and its types.

    Example:
        >>> extract_words_and_types("/home/user/repo_output", "/home/user/api_output.txt")
        [('word1', {'type1', 'type2'}), ('word2', {'type3', 'type4'})]
    """
    output_dir = repo_output_folder.split("/")[1]
    file_name = repo_output_folder.split("/")[2]
    fpath = output_dir + "/" + os.path.basename(path_api_output) + "/" + file_name
    with open(fpath, "r") as file:
        lines = file.readlines()

    result = []
    word = None
    types = []
    for line in lines:
        if line.startswith("^^"):
            if word is not None:
                result.append((word, types))
            word = line.split("^^")[1].strip()
            types = set()
        else:
            type_match = re.search(r"type: (\w+)", line)
            if type_match:
                types.add(type_match.group(1))
    if word is not None:
        result.append((word, types))

    api_call_set_path = (
        output_dir + "/" + os.path.basename(path_api_output) + "/" + "APICALLS.txt"
    )

    with open(f"{api_call_set_path}", "w") as file:
        for i in result:
            file.write(str(i) + "\n")
    return result


def filer_final_api_calls(repo_output_folder, filter, api_list):
    """
    Filter and write the final API calls to a file.

    Args:
        repo_output_folder (str): The path to the output folder.
        filter (str): The filter to apply to the API calls.
        api_list (list): The list of API calls.

    Returns:
        None
    """
    api_call_set_path = repo_output_folder + "/" + "filtered_api_calls.txt"

    with open(f"{api_call_set_path}", "w") as file:
        for i in api_list:
            if "function" in i[1]:
                file.write(str(i) + "\n")
    utilities.convert_and_write_to_json(
        repo_output_folder + "/" + "filtered_api_calls.txt",
        repo_output_folder + "/" + "filtered_api_calls.json",
    )
