import os
import shutil


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
    for line in file_line:
        line_count += 1
        if "public class" in line:
            print(" public class found: line: ", line)
            continue
        if line.strip() == "" or line.strip() == "\n":
            first_code_found = True
            continue
        if not first_code_found:
            first_code += line
        else:
            second_code += line
    second_code = second_code[:-2]
    print(first_code)
    print("\n\n\n==============\n\n")
    print(second_code)

    first_code_len = len(first_code.split("\n"))
    second_code_len = len(second_code.split("\n"))

    first_file_to_inject = "JHotDraw/application/DrawApplication.java"
    first_file_line_number = 101

    second_file_to_inject = "JHotDraw/applet/DrawApplet.java"
    second_file_line_number = 93

    shutil.copy(
        first_file_to_inject,
        "DrawApplication_main.java",
    )
    shutil.copy(
        second_file_to_inject,
        "DrawApplet_main.java",
    )

    insert_code(first_file_to_inject, first_file_line_number, first_code)
    insert_code(second_file_to_inject, second_file_line_number, second_code)

    from subprocess import call

    rc = rc = call("./run_deckard.sh", shell=True)

    first_lookup = []
    for i in range(0, int(first_code_len * 0.3)):
        counter = first_file_line_number + int(i)
        string = first_file_to_inject + " LINE:" + str(counter) + ":"
        first_lookup.append(string)

    second_lookup = []
    for i in range(0, int(second_code_len * 0.3)):
        counter = second_file_line_number + int(i)
        string = second_file_to_inject + " LINE:" + str(counter) + ":"
        second_lookup.append(string)

    counter = 0
    first_code_found = []
    second_code_found = []
    log_file = "clusters/post_cluster_vdb_30_2_allg_0.70_50"

    with open(
        log_file,
        "r",
    ) as f:
        for l in f.readlines():
            counter += 1
            for li in first_lookup:
                if li in l:
                    line_details = l.split(" ")
                    for ld in line_details:
                        if "LINE" in ld:
                            ld = ld.split(":")
                            if int(ld[-1]) > int(first_code_len * 0.7):
                                if int(ld[-2]) + int(ld[-1]) <= (
                                    first_file_line_number + first_code_len
                                ):
                                    first_code_found.append(counter)

    counter = 0
    with open(
        log_file,
        "r",
    ) as f:
        for l in f.readlines():
            counter += 1
            for li in second_lookup:
                if li in l:
                    line_details = l.split(" ")
                    for ld in line_details:
                        if "LINE" in ld:
                            ld = ld.split(":")
                            if int(ld[-1]) > int(second_code_len * 0.7):
                                if int(ld[-2]) + int(ld[-1]) <= (
                                    second_file_line_number + second_code_len
                                ):
                                    second_code_found.append(counter)

    print("first_code_found: ", first_code_found)
    print("second_code_found: ", second_code_found)

    from itertools import product

    closet_pair_result = sorted(
        product(first_code_found, second_code_found), key=lambda t: abs(t[0] - t[1])
    )

    print(closet_pair_result)

    with open(log_file) as f:
        log_lines = f.readlines()

    gap_found = False
    for pair in closet_pair_result:
        gap_found = False
        first_line = pair[0]
        second_line = pair[1]
        if first_line > second_line:
            sub_log = log_lines[second_line:first_line]
        else:
            sub_log = log_lines[first_line:second_line]

        print(len(sub_log))
        for sl in sub_log:
            print("sl: ", sl)
            if len(sl.strip()) == 0:
                print("sl gap: ", gap_found)
                gap_found = True
                break
        if not gap_found:
            break
    print("gap_found: ", gap_found)
    if not gap_found and (len(first_code_found) > 0 and len(second_code_found) > 0):
        clone_counter += 1
        print(file, " clone detected in the system ========= counter: ", clone_counter)

    os.remove(first_file_to_inject)
    os.remove(second_file_to_inject)

    shutil.copy(
        "DrawApplication_main.java",
        first_file_to_inject,
    )
    shutil.copy(
        "DrawApplet_main.java",
        second_file_to_inject,
    )
    break

print("clone_counter: ", clone_counter)

done = time.time()
print(done)
elapsed = done - start
print("time elapsed: ", elapsed)
