import os
import shutil
from subprocess import call
import pandas as pd
import time


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


start = time.time()
print(start)
main_dir = "data_folder_path"

filelist = sorted(os.listdir(main_dir))
fcc = 0
clone_counter = 0
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
    first_file_to_inject = "commonsym.c"
    first_file_line_number = 2

    second_file_to_inject = "chibicc/test/typeof.c"
    second_file_line_number = 2

    # making a copy of those file before injection
    shutil.copy(
        first_file_to_inject,
        "commonsym_main.c",
    )
    shutil.copy(
        second_file_to_inject,
        "typeof_main.c",
    )

    # injecting clone pair
    insert_code(first_file_to_inject, first_file_line_number, first_code)
    insert_code(second_file_to_inject, second_file_line_number, second_code)

    # running cccd
    rc = call(
        "./run_cccd.sh",
        shell=True,
    )

    first_lookup = "test/commonsym"
    second_lookup = "test/typeof"
    log_file = "chibicc/chibicc_comparisionReport.csv"

    chibicc_log_csv = pd.read_csv(log_file)
    first_code_f = chibicc_log_csv[chibicc_log_csv["Files"].str.contains(first_lookup)]
    first_code_f = first_code_f[first_code_f["Files"].str.contains(second_lookup)]

    if len(first_code_f) > 0:
        print("found both")
        leven_dis = first_code_f["LevenDistance"].values.tolist()[0]
        if leven_dis <= 35:
            print("both of them clone")
            clone_counter += 1
            print(
                file, " clone detected in the system ========= counter: ", clone_counter
            )
        else:
            print("not clone")

    else:
        print("first_code_len 0")

    # removing injected file
    os.remove(first_file_to_inject)
    os.remove(second_file_to_inject)
    os.remove(log_file)

    # copying the same file without injection
    shutil.copy(
        "commonsym_main.c",
        first_file_to_inject,
    )
    shutil.copy(
        "typeof_main.c",
        second_file_to_inject,
    )
    break

print("clone_counter: ", clone_counter)
done = time.time()
print(done)
elapsed = done - start
print("time elapsed: ", elapsed)
