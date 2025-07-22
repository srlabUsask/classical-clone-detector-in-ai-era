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


import time

start = time.time()
print(start)

main_dir = "data_path"

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

    first_file_to_inject = "django/django/contrib/admin/actions.py"
    first_file_line_number = 12
    second_file_to_inject = "django/django/apps/registry.py"
    second_file_line_number = 426

    # making a copy of those file before injection
    shutil.copy(
        first_file_to_inject,
        "actions_main.py",
    )
    shutil.copy(
        second_file_to_inject,
        "registry_main.py",
    )

    # injecting clone pair
    insert_code(first_file_to_inject, first_file_line_number, first_code)
    insert_code(second_file_to_inject, second_file_line_number, second_code)

    # running pmd
    rc = call("./run_pmd.sh", shell=True)

    # string to look for in pmd result log
    first_lookup = []
    for i in range(-1, int(first_code_len * 0.3)):
        counter = first_file_line_number + int(i)
        string = "Starting at line " + str(counter) + " of " + first_file_to_inject
        first_lookup.append(string)

    second_lookup = []
    for i in range(-1, int(second_code_len * 0.3)):
        counter = second_file_line_number + int(i)
        string = "Starting at line " + str(counter) + " of " + second_file_to_inject
        second_lookup.append(string)

    print("first_lookup: ", first_lookup)
    print("second_lookup: ", second_lookup)

    counter = 0
    first_code_found = []
    second_code_found = []
    log_file = "pmd_results.txt"

    # checking where first code fragment got detected in pmd log
    with open(
        log_file,
        "r",
    ) as f:
        for l in f.readlines():
            counter += 1
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

    print("first_code_found: ", first_code_found)
    print("second_code_found: ", second_code_found)

    # making pair of both code fragments occurance point
    from itertools import product

    closet_pair_result = sorted(product(first_code_found, second_code_found), key=lambda t: abs(t[0] - t[1]))

    print(closet_pair_result)

    with open(log_file) as f:
        log_lines = f.readlines()

    # checking if both code fragment occured in same clone pair location
    gap_found = False
    gap_finder = []
    final_decision_gap = True
    for pair in closet_pair_result:
        gap_found = False
        first_line = pair[0]
        second_line = pair[1]
        if abs(first_line - second_line) == 1:
            final_decision_gap = False
            break
        if first_line > second_line:
            sub_log = log_lines[second_line:first_line]
        else:
            sub_log = log_lines[first_line:second_line]

        print(len(sub_log))
        for sl in sub_log:
            print("sl: ", sl)
            if "=====================================================================" in sl:
                print("sl gap: ", gap_found)
                gap_found = True
                break

        gap_finder.append(gap_found)

    for i in gap_finder:
        if not i:
            final_decision_gap = False
            break

    # printing if both clone pair showed up together
    print("final_decision_gap: ", final_decision_gap)
    if not final_decision_gap and (len(first_code_found) > 0 and len(second_code_found) > 0):
        clone_counter += 1
        print(file, " clone detected in the system ========= counter: ", clone_counter)

    # removing injected file
    os.remove(first_file_to_inject)
    os.remove(second_file_to_inject)

    # copying the same file without injection
    shutil.copy(
        "actions_main.py",
        first_file_to_inject,
    )
    shutil.copy(
        "registry_main.py",
        second_file_to_inject,
    )
    break

print("clone_counter: ", clone_counter)
done = time.time()
print(done)
elapsed = done - start
print("time elapsed: ", elapsed)
