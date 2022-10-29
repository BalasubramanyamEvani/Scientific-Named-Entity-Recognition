import re
import os


def remove_middle_columns(conll_content: str):
    conll_content = conll_content.strip()
    conll_content = conll_content.replace(" -X- _ ", "\t")
    return conll_content


if __name__ == "__main__":
    conll_data_path = os.path.join(os.getcwd(), "data", "conll")
    files = os.listdir(conll_data_path)
    files = [file for file in files if file.endswith(".conll")]
    files = sorted(files)
    train_set = []
    for file in files:
        with open(os.path.join(conll_data_path, file), "r") as f:
            curr_conll_content = remove_middle_columns(f.read())
            train_set.append(curr_conll_content)

    train_set = "\n".join(train_set)
    train_set = train_set.replace("-DOCSTART- -X- O", "")
    train_set = train_set.strip()
    train_set_conll_path = os.path.join(conll_data_path, f"ner_dataset.conll")
    with open(train_set_conll_path, "w") as fd:
        fd.write(train_set)
