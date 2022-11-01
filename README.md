## ANLP HW - 2 NER System from Scratch

---

### Team Members: Balasubramanyam Evani, Neel Pawar

This repository contains our implementation of building a NER system from the ground up.

The full process we followed is as follows:

1. [Collecting Research paper PDFs](#collecting-research-paper-pdfs)
2. [Downloading and Parsing PDF](#downloading-and-parsing-pdf)
3. [Annotate test and training data for development](#annotating-data)
4. [NER System](#ner-system)

## Collecting Research Paper PDFs

We have primarily used researched papers scraped from Arxiv and ACL Anthology. We did this by creating a script which automatically scrapes research paper information from the respective websites.

After scraping information from Arxiv and ACL Anthology using our defined queries we created a **csv** file. This **csv** file was then used to download research paper pdfs and parse the downloaded pdfs

In order to follow the below process

```
python pdf_data_collect.py
```

This would generate a **csv** with name **ner_task_pdf_links.csv** file with the following columns:

- **from**: arxiv or acl_anthology
- **title**: paper title
- **authors**: paper authors
- **published**: publish data
- **journal_ref**: which journal it was published in - not always present
- **summary**: summary of the paper
- **pdf_url**: pdf url of the research paper

## Downloading And Parsing PDF

Once relevant papers have been downloaded we can then make use of utility functions defined in the **ner_preprocessing.ipynb** notebook to:

- **Download PDF**: make use of the **download_pdf** function for this
- **Data Preparation**: Extracting text from PDFs, make use of **process_pdf_data** function
  - Before running this function make sure to run the grobid server (more info at https://github.com/titipata/scipdf_parser)

## Annotating Data

Once the PDF text has been parsed and extracted we have used Label Studio to annotate data. For a particular paper the text extracted in the previous process was extracted at paragraph level. Hence, multiple tasks would be created for a single PDF when imported to Label Studio.

Labels and Label Standards were followed as mentioned in https://github.com/neubig/nlp-from-scratch-assignment-2022/blob/main/annotation_interface.md

## NER System

### Creating Dataset

In order to create train, our own test datasets one case make use of the following script.

```
python create_dataset_script.py
```

This script is run to generate train and test datasets. For the current implementation we have selected one of the papers which we had annotated namely "XLNet" to be the test set and all other conll files is grouped into train set.

Two trainsets are generated namely **ner_dataset_one_left_out.conll** and **full_ner_dataset.conll**. The difference between the two generated files is the inclusion
of "XLNet.conll" in the latter.

The **ner_dataset_one_left_out.conll** is used for building a model and then tested on
**XLNet.conll**. One thing to note is for our own final test set (XLNet.conll) we reduced the generated ground truth to limit to only 1417 lines. This was not a very robust which but just a sample test sequence which we wanted to test.

Once satisfactory results were observed we accumulated all the data in
**full_ner_dataset.conll** to build the final model.

### Running the NER notebook

Given the folder structure in this repository is maintained we can sequentially run the **ner.ipynb** notebook to obtain the results showed in our report.

In the notebook we have explored a total of 3 pretrained models which we finetuned for our train dataset:

1. BERT BASE CASED
2. SCIBERT CASED
3. SCIBERT UNCASED
