from model import Model
from transformers import RobertaConfig, RobertaModel, RobertaTokenizer
import torch
import seaborn as sns
import os
from tqdm.notebook import tqdm
import re
import tqdm

device = torch.device("cpu")


def replacer(match):
    s = match.group(0)
    if s.startswith("/"):
        return " "  # note: a space and not an empty string
    else:
        return s


def remove_comments_and_docstrings(code):
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE,
    )
    temp = []
    for x in re.sub(pattern, replacer, code).split("\n"):
        if x.strip() != "":
            temp.append(x)
    return "\n".join(temp)


def convert_examples_to_features(code_1, code_2, remove_comments, b_size=400):
    if remove_comments:
        code_1 = remove_comments_and_docstrings(code_1)
        code_2 = remove_comments_and_docstrings(code_2)

    code1_tokens = tokenizer.tokenize(code_1)
    code1_tokens = code1_tokens[: b_size - 2]
    code1_tokens = [tokenizer.cls_token] + code1_tokens + [tokenizer.sep_token]
    code1_ids = tokenizer.convert_tokens_to_ids(code1_tokens)
    padding_length = b_size - len(code1_ids)
    code1_ids += [tokenizer.pad_token_id] * padding_length

    code2_tokens = tokenizer.tokenize(code_2)
    code2_tokens = code2_tokens[: b_size - 2]
    code2_tokens = [tokenizer.cls_token] + code2_tokens + [tokenizer.sep_token]
    code2_ids = tokenizer.convert_tokens_to_ids(code2_tokens)
    padding_length = b_size - len(code2_ids)
    code2_ids += [tokenizer.pad_token_id] * padding_length
    source_ids = code1_ids + code2_ids
    return torch.tensor(source_ids).to(device)


config = RobertaConfig.from_pretrained("roberta-base")
model = RobertaModel.from_pretrained("microsoft/codebert-base")
tokenizer = RobertaTokenizer.from_pretrained("roberta-base")

model = Model(model, config, tokenizer)

model_path = "CodeBERT_model.bin"
model.load_state_dict(torch.load(model_path, map_location=lambda storage, loc: storage), strict=False)
model.to(device)


folder_list = ["folder_list"]

for main_dir in folder_list:
    remove_comments = True
    predictions = []
    filelist = sorted(os.listdir(main_dir))
    fcc = 0
    clone_counter = 0
    for file in tqdm.tqdm(filelist):
        fcc += 1
        file_line = open(main_dir + "/" + file, "r")
        line_count = 0
        first_code = ""
        second_code = ""
        first_code_found = False
        for line in file_line:
            line_count += 1
            if line.strip() == "" or line.strip() == "\n":
                first_code_found = True
                continue
            if not first_code_found:
                first_code += line
            else:
                second_code += line

        first_code = first_code.split("\n")
        first_code.pop(0)
        first_code = "\n".join(first_code)

        second_code = second_code.split("\n")
        second_code.pop(0)
        second_code = "\n".join(second_code)

        iput_ids = convert_examples_to_features(first_code, second_code, remove_comments)
        prediction = model(iput_ids)
        prediction = int(torch.argmax(prediction[0]))
        predictions.append(prediction)

    print("detected: ", predictions.count(1))
    print("not detected: ", predictions.count(0))
