import re
import os


def remove_middle_columns(conll_content: str):
    conll_content = conll_content.strip()
    conll_content = conll_content.replace(" -X- _ ", "\t")
    return conll_content


if __name__ == "__main__":
    conll_files_filter = set(["full_ner_dataset.conll",
                              "ner_dataset_one_left_out.conll"])

    own_test_set_name = "XLNet.conll"
    conll_data_path = os.path.join(os.getcwd(), "data", "conll")

    files = os.listdir(conll_data_path)
    files = [file for file in files if file.endswith(
        ".conll") if file not in conll_files_filter]
    files = sorted(files)

    full_train_set = []
    train_set_without_own_test_set = []
    own_test_set = None

    for file in files:
        with open(os.path.join(conll_data_path, file), "r") as f:
            curr_conll_content = remove_middle_columns(f.read())
            full_train_set.append(curr_conll_content)
            if file != own_test_set_name:
                train_set_without_own_test_set.append(curr_conll_content)
            if file == own_test_set_name:
                own_test_set = re.split(r"\n\t?\n", curr_conll_content)
                own_test_set = "\n".join(own_test_set[::-1])

    full_train_set = "\n".join(full_train_set)
    train_set_without_own_test_set = "\n".join(train_set_without_own_test_set)

    full_train_set = full_train_set.replace("-DOCSTART- -X- O", "")
    full_train_set = full_train_set.strip()

    train_set_without_own_test_set = train_set_without_own_test_set.replace(
        "-DOCSTART- -X- O", "")
    train_set_without_own_test_set = train_set_without_own_test_set.strip()

    own_test_set = own_test_set.replace(
        "-DOCSTART- -X- O", "")
    own_test_set = own_test_set.strip()

    full_train_set_conll_path = os.path.join(
        conll_data_path, f"full_ner_dataset.conll")
    with open(full_train_set_conll_path, "w") as fd:
        fd.write(full_train_set)

    train_set_without_own_test_set_path = os.path.join(
        conll_data_path, f"ner_dataset_one_left_out.conll")
    with open(train_set_without_own_test_set_path, "w") as fd:
        fd.write(train_set_without_own_test_set)

    own_test_set_path = os.path.join(
        os.getcwd(), "data", "own_test_set", f"XLNet.conll")
    with open(own_test_set_path, "w") as fd:
        fd.write(own_test_set)
