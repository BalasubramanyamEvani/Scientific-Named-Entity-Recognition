"""
This script is run to generate train and test datasets. For the current implementation
we have selected one of the papers which we had annotated namely "XLNet" to be the test
set and all other conll files is grouped into train set.

Two trainsets are generated namely "ner_dataset_one_left_out.conll" and 
"full_ner_dataset.conll". The difference between the two generated files is the inclusion 
of "XLNet.conll" in the latter. 

The "ner_dataset_one_left_out.conll" is used for building a model and then tested on
"XLNet.conll". Once satisfactory results were observed we accumulated all the data in
"full_ner_dataset.conll" to build the final model.
"""
import re
import os


def remove_middle_columns(conll_content: str):
    """
    This function accepts the conll content removes any unwanted whitespace 
    at the start and end along with the middle two columns that gets generated 
    when exporting from Label Studio

    Sample Example: 

    Acknowledgements -X- _ O -> Acknowledgements    O

    Args:
        conll_content (str): The conll content as string

    Returns:
        str: filtered conll content
    """
    conll_content = conll_content.strip()
    conll_content = conll_content.replace(" -X- _ ", "\t")
    return conll_content


if __name__ == "__main__":
    # required to not include old dataset
    conll_files_filter = set(["full_ner_dataset.conll",
                              "ner_dataset_one_left_out.conll"])

    # used as test set
    own_test_set_name = "XLNet.conll"

    # the directory where all the conll files are stored
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

    # removing docstart headers
    full_train_set = full_train_set.replace("-DOCSTART- -X- O", "")
    full_train_set = full_train_set.strip()

    train_set_without_own_test_set = train_set_without_own_test_set.replace(
        "-DOCSTART- -X- O", "")
    train_set_without_own_test_set = train_set_without_own_test_set.strip()

    own_test_set = own_test_set.replace(
        "-DOCSTART- -X- O", "")
    own_test_set = own_test_set.strip()

    # writing the generated train sets and test set and storing in the same
    # data directory

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
