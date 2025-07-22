import os
import shutil
from subprocess import call


def insert_code(file: str, index: int, value: str) -> None:
    """insert code in desired location

    Args:
        file (str): targeted file location
        index (int): from which line to inject
        value (str): code fragment to inject
    """

    with open(file, "r", encoding="utf-8", errors="ignore") as f:
        contents = f.readlines()

    contents.insert(index, value)

    with open(file, "w", encoding="utf-8", errors="ignore") as f:
        contents = "".join(contents)
        f.write(contents)


def find_str(s: str, char: str) -> int:
    """return index of substring from a string

    Args:
        s (str): main string
        char (str): substring

    Returns:
        int: location of substring in that string
    """

    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index : index + len(char)] == char:
                    return index

            index += 1

    return -1


import time

start = time.time()
print(start)

main_dir = "data_path"

filelist = sorted(os.listdir(main_dir))
fcc = 0
clone_counter = 0
failed_counter = 0
syntax_prob = []
for file in filelist:
    fcc += 1
    file_line = open(main_dir + "/" + file, "r")
    line_count = 0
    first_code = ""
    second_code = ""
    first_code_found = False

    # fetching 2 code fragments
    for line in file_line:
        line_count += 1
        if line.strip() == "" or line.strip() == "\n":
            first_code_found = True
            continue
        if not first_code_found:
            first_code += line
        else:
            second_code += line

    print(first_code)
    print("\n\n\n==============\n\n")
    print(second_code)

    # fetching lenght of 2 code fragments
    first_code_len = len(first_code.split("\n"))
    second_code_len = len(second_code.split("\n"))

    # location to inject clone pair
    first_file_to_inject = "SmoothStream/StreamViewer.py"
    first_file_line_number = 53

    second_file_to_inject = "SmoothStream/Streamer.py"
    second_file_line_number = 56

    # making a copy of those file before injection
    shutil.copy(
        first_file_to_inject,
        "StreamViewer_main.py",
    )
    shutil.copy(
        second_file_to_inject,
        "Streamer_main.py",
    )

    # injecting clone pair
    insert_code(first_file_to_inject, first_file_line_number, first_code)
    insert_code(second_file_to_inject, second_file_line_number, second_code)

    # running clonedigger
    rc = call("./run_clonedigger.sh", shell=True)

    # string to look for in pmd result log
    first_lookup = []
    for i in range(-1, int(first_code_len * 0.3)):
        counter = first_file_line_number + int(i)
        string = "SmoothStream/StreamViewer.py"
        first_lookup.append(string)

    second_lookup = []
    for i in range(-1, int(second_code_len * 0.3)):
        counter = second_file_line_number + int(i)
        string = "SmoothStream/Streamer.py"
        second_lookup.append(string)

    print("first_lookup: ", first_lookup)
    print("second_lookup: ", second_lookup)

    counter = 0
    first_code_found = []
    second_code_found = []
    log_file = "output.html"

    # checking where first code fragment got detected in pmd log
    with open(
        log_file,
        "r",
    ) as f:
        for l in f.readlines():
            counter += 1
            if "SyntaxError: invalid syntax" in l:
                print("syntax error happened: ")
                print("can not processed by clone digger: ", file)
                failed_counter += 1
                syntax_prob.append(file)
            for li in first_lookup:
                if li in l:
                    first_code_found.append(counter)

    # checking where second code fragment got detected in pmd log
    counter = 0
    with open(
        log_file,
        "r",
    ) as f:
        for l in f.readlines():
            counter += 1
            for li in second_lookup:
                if li in l:
                    second_code_found.append(counter)

    first_code_found = list(set(first_code_found))
    second_code_found = list(set(second_code_found))

    print("first_code_found: ", first_code_found)
    print("second_code_found: ", second_code_found)
    found_loc = -1

    first_occured = False

    for f_counter in range(0, len(first_code_found)):
        if first_code_found[f_counter] in second_code_found:
            if first_occured:
                found_loc = f_counter
                break
            else:
                first_occured = True
    print("found_loc: ", found_loc)

    with open(log_file) as f:
        log_lines = f.readlines()
    try:
        if found_loc > -1:
            sub_log = log_lines[first_code_found[found_loc] - 1]
            print("sub_log: ", sub_log)

            line_num_1 = find_str(sub_log, "The first line is ") + len(
                "The first line is "
            )

            line_num_2 = find_str(sub_log, "</TD><TD></TD><TD>Source file ")

            start_line = int(sub_log[line_num_1:line_num_2])

            valid_line_number = [52, 53, 54, 55, 56, 57]

            print("line_num_1: ", line_num_1)
            print("line_num_2: ", line_num_2)

            print(
                "int(sub_log[line_num_1:line_num_2]) : ",
                sub_log[line_num_1:line_num_2],
            )

            if start_line in valid_line_number:
                clone_size_loc = find_str(sub_log, "Clone size = ") + len(
                    "Clone size = "
                )

                table_tag_starts = find_str(sub_log, "<TABLE ")

                print("clone_size_loc: ", clone_size_loc)
                print("table_tag_starts: ", table_tag_starts)

                print("sub_log[l1:l2]: ", sub_log[clone_size_loc:table_tag_starts])

                clone_size = int(sub_log[clone_size_loc:table_tag_starts])

                if clone_size >= (int(first_code_len * 0.7)) or clone_size >= (
                    int(second_code_len * 0.7)
                ):
                    print("clone found")
                    clone_counter += 1
                    print(
                        file,
                        " clone detected in the system ========= counter: ",
                        clone_counter,
                    )

            else:
                print("invalid start line")
        else:
            print("clone not found")
    except Exception as e:
        print("parse error happened: ", e)
        print("can not processed by clone digger: ", file)
        failed_counter += 1
        syntax_prob.append(file)

    # removing injected file
    os.remove(first_file_to_inject)
    os.remove(second_file_to_inject)
    os.remove(log_file)

    # copying the same file without injection
    shutil.copy(
        "StreamViewer_main.py",
        first_file_to_inject,
    )
    shutil.copy(
        "Streamer_main.py",
        second_file_to_inject,
    )
    break

print("\n\n\n\n\n====================================================")
print("clone_counter: ", clone_counter)
print("failed_counter: ", failed_counter)
print("syntax_prob: ", syntax_prob)


done = time.time()
print(done)
elapsed = done - start
print("time elapsed: ", elapsed)
