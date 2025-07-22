import os
import shutil
import json
import pandas as pd


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


def main():
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
        try:
            for line in file_line:
                line_count += 1
                """# if running semanticclonebench java clones, uncomment this part
                if "public class" in line:
                    print(" public class found: line: ", line)
                    continue
                """
                if line.strip() == "" or line.strip() == "\n":
                    first_code_found = True
                    continue
                if not first_code_found:
                    first_code += line
                else:
                    second_code += line
        except Exception as e:
            print("code byte error happened: file: ", file)
            continue
        """# if running SemanticCloneBench java clones, uncomment this part
        second_code = second_code[:-2]
        """
        print(first_code)
        print("\n\n\n==============\n\n")
        print(second_code)

        first_code_len = len(first_code.split("\n"))
        second_code_len = len(second_code.split("\n"))

        first_file_to_inject = "SmoothStream/StreamViewer.py"
        first_file_line_number = 53

        second_file_to_inject = "SmoothStream/Streamer.py"
        second_file_line_number = 56

        shutil.copy(
            first_file_to_inject,
            "StreamViewer_main.py",
        )
        shutil.copy(
            second_file_to_inject,
            "Streamer_main.py",
        )

        insert_code(first_file_to_inject, first_file_line_number, first_code)
        insert_code(second_file_to_inject, second_file_line_number, second_code)

        from subprocess import call

        _ = call("./run_cloneworks.sh", shell=True)

        first_code_file = -1
        second_code_file = -1

        with open(
            "SmoothStream.files",
            "r",
        ) as f:
            for l in f.readlines():
                if l.startswith("#"):
                    continue
                if "StreamViewer.py" in l:
                    first_code_file = int(l.split("\t")[0])
                elif "Streamer.py" in l:
                    second_code_file = int(l.split("\t")[0])

        if first_code_file == -1 or second_code_file == -1:
            print("could not able to find the file")
            os.remove(first_file_to_inject)
            os.remove(second_file_to_inject)
            os.remove("SmoothStream.files")
            os.remove("SmoothStream.fragments")
            os.remove("SmoothStream.clones")

            shutil.copy(
                "StreamViewer_main.py",
                first_file_to_inject,
            )
            shutil.copy(
                "Streamer_main.py",
                second_file_to_inject,
            )
            continue

        first_lookup = []
        for i in range(-1, 4):
            counter = first_file_line_number + int(i)
            string = str(first_code_file) + "," + str(counter) + ","
            first_lookup.append(string)

        second_lookup = []
        for i in range(-1, 4):
            counter = second_file_line_number + int(i)
            string = str(second_code_file) + "," + str(counter) + ","
            second_lookup.append(string)

        log_file = "SmoothStream.clones"

        with open(
            log_file,
            "r",
        ) as f:
            for l in f.readlines():
                first_part_found = False
                if l.startswith("#"):
                    continue
                l_arr = l.split(",")
                first_code_lookup = ",".join([l_arr[0], l_arr[1]]) + ","
                second_code_lookup = ",".join([l_arr[3], l_arr[4]]) + ","

                # search in first part
                for fl in first_lookup:
                    if fl in first_code_lookup:
                        first_part_found = True
                        for sl in second_lookup:
                            if sl in second_code_lookup:
                                clone_counter += 1
                                print(
                                    file,
                                    " clone detected in the system ========= counter: ",
                                    clone_counter,
                                )

                if not first_part_found:
                    # search in second part
                    for fl in first_lookup:
                        if fl in second_code_lookup:
                            for sl in second_lookup:
                                if sl in first_code_lookup:
                                    clone_counter += 1
                                    print(
                                        file,
                                        " clone detected in the system ========= counter: ",
                                        clone_counter,
                                    )

        os.remove(first_file_to_inject)
        os.remove(second_file_to_inject)
        os.remove("SmoothStream.files")
        os.remove("SmoothStream.fragments")
        os.remove("SmoothStream.clones")

        shutil.copy(
            "StreamViewer_main.py",
            first_file_to_inject,
        )
        shutil.copy(
            "Streamer_main.py",
            second_file_to_inject,
        )

        print("file_deleted")
        break

    print("clone_counter: ", clone_counter)
    done = time.time()
    print(done)
    elapsed = done - start
    print("time elapsed: ", elapsed)


def semanticCloneBench():
    url_to_code = {}
    with open("data_json.json") as f:
        for line in f:
            line = line.strip()
            js = json.loads(line)
            url_to_code[js["idx"]] = js["func"]

    data_t = pd.read_csv("data_csv")
    # data = data_t[data_t["labels"] == 1]
    clone_types = ["type-3-strong", "type-3-medium", "type-3-weak"]

    for ct in clone_types:
        data = data_t[data_t["syntactic_types"] == ct]

        code_ids = data["code_ids"].values.tolist()
        labels = data["labels"].values.tolist()
        print(len(code_ids))
        print(len(labels))
        clone_counter = 0
        for ids, _ in zip(code_ids, labels):
            ids = ids.replace("(", "")
            ids = ids.replace(")", "")
            ids = ids.replace("'", "")
            ids = ids.replace(" ", "")
            ids = ids.split(",")
            first_code = url_to_code[str(ids[0])]
            second_code = url_to_code[str(ids[1])]
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

            rc = call("./run_cloneworks.sh", shell=True)

            first_code_file = -1
            second_code_file = -1

            with open(
                "JHotDraw.files",
                "r",
            ) as f:
                for l in f.readlines():
                    if l.startswith("#"):
                        continue
                    if "application/DrawApplication.java" in l:
                        first_code_file = int(l.split("\t")[0])
                    elif "applet/DrawApplet.java" in l:
                        second_code_file = int(l.split("\t")[0])

            if first_code_file == -1 or second_code_file == -1:
                print("could not able to find the file")
                os.remove(first_file_to_inject)
                os.remove(second_file_to_inject)
                os.remove("JHotDraw.files")
                os.remove("JHotDraw.fragments")
                os.remove("JHotDraw.clones")

                shutil.copy(
                    "DrawApplication_main.java",
                    first_file_to_inject,
                )
                shutil.copy(
                    "DrawApplet_main.java",
                    second_file_to_inject,
                )
                continue

            first_lookup = []
            for i in range(-1, 3):
                counter = first_file_line_number + int(i)
                string = str(first_code_file) + "," + str(counter) + ","
                first_lookup.append(string)

            second_lookup = []
            for i in range(-1, 3):
                counter = second_file_line_number + int(i)
                string = str(second_code_file) + "," + str(counter) + ","
                second_lookup.append(string)

            log_file = "JHotDraw.clones"

            with open(
                log_file,
                "r",
            ) as f:
                for l in f.readlines():
                    first_part_found = False
                    if l.startswith("#"):
                        continue
                    l_arr = l.split(",")
                    first_code_lookup = ",".join([l_arr[0], l_arr[1]]) + ","
                    second_code_lookup = ",".join([l_arr[3], l_arr[4]]) + ","

                    # search in first part
                    for fl in first_lookup:
                        if fl in first_code_lookup:
                            first_part_found = True
                            for sl in second_lookup:
                                if sl in second_code_lookup:
                                    clone_counter += 1
                                    print(
                                        ids,
                                        " clone detected in the system ========= counter: ",
                                        clone_counter,
                                    )

                    if not first_part_found:
                        # search in second part
                        for fl in first_lookup:
                            if fl in second_code_lookup:
                                for sl in second_lookup:
                                    if sl in first_code_lookup:
                                        clone_counter += 1
                                        print(
                                            ids,
                                            " clone detected in the system ========= counter: ",
                                            clone_counter,
                                        )

            os.remove(first_file_to_inject)
            os.remove(second_file_to_inject)
            os.remove("JHotDraw.files")
            os.remove("JHotDraw.fragments")
            os.remove("JHotDraw.clones")

            shutil.copy(
                "DrawApplication_main.java",
                first_file_to_inject,
            )
            shutil.copy(
                "DrawApplet_main.java",
                second_file_to_inject,
            )

            print("file_deleted")

        print(
            "%%%%%%%%%%%%%\n\nType: ",
            ct,
            " clone_counter: ",
            clone_counter,
            " %%%%%%%%%%%%%\n\n",
        )


main()
