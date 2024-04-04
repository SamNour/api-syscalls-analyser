#! /usr/bin/env python3
import os
import re
import cli
import utilities
from Trie import Trie
from pygments import lex
from collections import deque
from pygments.lexers import CLexer


SYSCALLS_EXTRACTED_FROM_C_CPP_FILES, FOUND_SYSCALLS, headers_set = set(), set(), set()
INCLUDE_PATTERN = re.compile(r"#\s*include\s+<(.+?)>")
DEFINE_PATTERN = re.compile(r"#\s*define\s+<(.+?)>")
COMPILER_PATH = (
    "/opt/rta-vrte-linux/3.8.0/sysroots/aarch64-boschdenso-linux/usr/include"
)
HEADERS_SET_SIZE = 0


def x86_64_syscalls() -> set():
    """
    Retrieves x86_64 system calls from the 'strace_calls.txt' file.

    Returns:
        A set containing the x86_64 system calls.
    """
    syscalls_1_2 = set()
    with open("strace_calls.txt", "r") as f:
        data = f.read()
    lines = data.split("\n")
    pattern = r"\d+\s+(\w+)\s+"
    for line in lines:
        match = re.search(pattern, line)
        if match:
            syscalls_1_2.add(match.group(1))
    return syscalls_1_2


def find_c_cpp_files(directory: dict()) -> set():
    """
    Find all C and C++ files in the specified directory and its subdirectories.

    Args:
        directory (str): The directory to search for C and C++ files.

    Returns:
        set: A set of absolute file paths for all C and C++ files found.
    """
    c_cpp_files = set()
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith((".c", ".cpp")):
                file_path = os.path.join(root, filename)
                c_cpp_files.add(os.path.abspath(file_path))
    return c_cpp_files


def preprocess_and_save(repo_path: str()):
    """
    Preprocesses all C and C++ files in the given repository path and saves the preprocessed output.

    Args:
        repo_path (str): The path to the repository.

    Returns:
        None
    """
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith((".c", ".cpp")):
                file_path = os.path.join(root, file)
                file_name, _ = os.path.splitext(file_path)
                output_file = file_name + (
                    "_preprocessed.c" if file.endswith(".c") else ".o"
                )
                os.system(f"gcc -E {file_path} -o {output_file}")


def find_words_in_file(file_path: str(), words_to_find: set()):
    """
    Finds and extracts words from a file that match the given set of words.

    Args:
        file_path (str): The path to the file to be searched.
        words_to_find (set): A set of words to be searched for in the file.

    Returns:
        set: A set of words extracted from the file that match the given set of words.
    """
    with open(file_path, "r") as file:
        for line in file:
            words_in_line = line.split()
            for word in words_in_line:
                if word in words_to_find:
                    SYSCALLS_EXTRACTED_FROM_C_CPP_FILES.add(word)
    return SYSCALLS_EXTRACTED_FROM_C_CPP_FILES


def syscall_hunter(syscalls: set(), c_cpp_file: dict()):
    """
    Searches for occurrences of specified syscalls in a C/C++ file.

    Args:
        syscalls (set): A set of syscalls to search for.
        c_cpp_file (dict): A dictionary containing the file path of the C/C++ file.

    Returns:
        set: A set of found syscalls.

    """
    with open(c_cpp_file, "r") as file:
        code = file.read()
    pattern = r"\b(" + "|".join(syscalls) + r")\s*\("
    matches = re.findall(pattern, code)
    FOUND_SYSCALLS.update(matches)
    return FOUND_SYSCALLS


# Using lexer
def extract_included_headers(file_path):
    """
    Extracts the included headers from a given file.

    Args:
        file_path (str): The path to the file.

    Returns:
        list: A list of included headers.

    """
    with open(file_path, "r") as file:
        code = file.read()

    lexer = CLexer()
    tokens = list(lex(code, lexer))

    headers = []
    for token_type, value in tokens:
        if "Token.Comment.PreprocFile" in str(token_type):
            headers.append(value[1:-1])
    return headers


# TODO: test lexer
# !Current wokring version
def header_hunter_lexer(list_of_c_cpp_files: list()) -> set():
    """
    Extracts included headers from a list of C/C++ files and returns a set of unique headers.

    Args:
        list_of_c_cpp_files (list): A list of file paths to C/C++ files.

    Returns:
        set: A set of unique headers extracted from the files.

    Raises:
        FileNotFoundError: If a header file is not found.

    """
    q = deque()
    processed_headers = set()  # to avoid processing the same header twice
    for file_path in list_of_c_cpp_files:
        try:
            list_headers = extract_included_headers(file_path)
            for i in list_headers:
                if i not in processed_headers:
                    q.append(i)
                    headers_set.add(i)

        except FileNotFoundError:
            print(f"Header not found: {file_path}")
    while q:
        header = q.pop()
        processed_headers.add(header)  # Mark header as processed
        if header.endswith(".h"):
            header_path = os.path.join(COMPILER_PATH, header)
            if os.path.exists(header_path):
                try:
                    with open(header_path, "r") as header_file:
                        for line in header_file:
                            match = INCLUDE_PATTERN.match(line) or DEFINE_PATTERN.match(
                                line
                            )
                            if match:
                                header = match.group(1)
                                if header not in processed_headers:
                                    q.append(header)
                                    headers_set.add(header)

                except:
                    print(f"Header file not found: {header_path}")
    return headers_set


def searching_for_syscalls_in_headers(
    syscalls_set: set(), headers_set: set(), header_directory: set
):
    """
    Searches for syscalls in header files.

    Args:
        syscalls_set (set): Set of syscalls to search for.
        headers_set (set): Set of header files to search in.
        header_directory (set): Directory where the header files are located.

    Returns:
        dict: A dictionary mapping each syscall to a set of headers where it is found.
    """
    syscall_to_headers_mapping = {}
    header_trie = Trie()

    for header in headers_set:
        if header.endswith(".h"):
            header_path = os.path.join(header_directory, header)

            if os.path.exists(header_path) and not header_trie.search(header_path):
                with open(header_path, "r") as header_file:
                    header_content = header_file.read()
                    header_trie.insert(header_path)

                    for syscall in syscalls_set:
                        if syscall in header_content:
                            if syscall not in syscall_to_headers_mapping:
                                syscall_to_headers_mapping[syscall] = set()
                            syscall_to_headers_mapping[syscall].add(header)
            else:
                print(f"Header file not found: {header_path}")
    return syscall_to_headers_mapping


def find_line_number_in_c_cpp(c_cpp_files, word_to_find):
    """
    Find the line numbers in C/C++ files where a specific word is found.

    Args:
        c_cpp_files (list): A list of C/C++ file paths.
        word_to_find (str): The word to search for in the files.

    Returns:
        dict: A dictionary where the keys are the file paths and the values are lists of line numbers
              where the word is found in each file.
    """
    dict = {}
    for file in c_cpp_files:
        dict[file] = utilities.grep_exact(word_to_find, file)
    return dict


if __name__ == "__main__":
    cli.run()
