# Jewish Studies -  State of the Field

### Contents
```
├── jstor_data/
|
├── citation_network.ipynb
├── csv_creation.ipynb
├── csv_prep.ipynb
├── data_cleaning_ipynb
├── data_separator.ipynb
├── dfr_topicmodling.ipynb
├── gender_visualization.ipynb
├── make_citations_ipynb
├── network_visualization.ipynb
├── sparklines.ipynb
|
├── csv_cleaning.py
├── ngram_visualization.py
├── unigram_analysis.py
|
├── custom_stopwords.txt
├── requirements.txt
|
├── LICENSE
└── README.md
```

### **Introduction**

This repository contains the code, description of workflows, and selected data files for our project investigating the journal <i>AJS Review</i> (the official publication of the [Association for Jewish Studies](https://www.associationforjewishstudies.org/)) from its founding to 2014, the last date for which we could acquire data.  The project has two goals: (1) To conduct analyses - particularly about the gender of the authors; trending words; topic modelling; and citation analysis - of the AJS Review in order to see if we can learn anything about the state of the academic field of Jewish studies and the way it has changed through time, and (2) to create a toolkit that more generally can be used to do similar analyses on other journals.

### Data

Our original plan was to "plug and play" with the scripts that Andrew Goldstone used for his [topic modelling of the *PMLA*](https://agoldst.github.io/dfr-browser/demo/).  This project is based on the [JSTOR Data for Research service](https://www.jstor.org/dfr/) (DfR).  It turns out that since the development of that set of scripts, DfR has changed the way in which they deliver their data, so we found, modified, and created several scripts (all found in this repository) that work with DfR data as it is currently (May, 2020) delivered.

We requested the full data for the full run of *AJS Review*.  This required filling out a form and then agreeing to certain licensing restrictions for the data (e.g., we cannot redistribute it).  Once we agreed, we were sent a link to download a zipped file.  When extracted, the file unpacks into five folders: metadata; ngram1; ngram2; ngram3; and ocr.  The metadata folder contains xml files; the others are text files.  The names of all the files are, fortunately, identical other than their extension or ending (e.g., journal-article-10.2307.1486231.xml; journal-article-10.2307.1486231.ngram1.txt; journal-article-10.2307.1486231.txt).  All the files that share a particular id are a single research article, book review, or something else (called "miscellaneous," e.g., front matter) - the metadata xml files helpfully indicates which of these three types it is.  

Ngram files consist of a list of words and the number of times that each word appears in the file, sorted by frequency and, within frequency, alphabetically.

The ocr files are the full text files, with the earlier files converted through ocr.  The ones that we used were quite messy and so required some cleaning (process indicated below) for use.

### Creation of a CSV Reference File from the XML Metadata Files

Our first step was to create a clean version of a CSV reference file from the XML files in the "metadata" folder.  We did this in the following steps:

1. Using the `csv_creation` notebook, we turned the XML files in the `jstor_data/metadata` directory into one CSV file saved in the main directory, called `articles_raw.csv`.
2.  We then used the `csv_prep` notebook to remove miscellaneous articles and infer the authors' genders. The output of this notebook is called `articles_gender.csv`.

### Gender Analysis

With `articles_raw.csv`, we used the `csv_prep` notebook which uses the library `gender_guesser` to look at the forenames in the author field and use its estimation of whether the name is male, female, most likely one or the other, equally likely to be either, or unknown.  141 articles were labeled with unknown names (some of these were in Hebrew); 6 were most likely male; 8 were most likely female; 5 were equally likely to be either (returning the value "andy"); and there were three stray files.  The uncorrected file is  `articles_gender.csv`.  We manually fixed those designations (and made some corrections to the gender identifications) and saved the file to `articles_gender_validated.csv`.

The `gender_visualization` notebook produces visualizations of author counts by gender and by year, conditioned on article type.  It takes in the file `articles_gender_validated.csv`and produces six visualizations:

1. `gender_by_year_all.png`: Number of Authors by Gender and Year (All Articles)
2. `gender_by_year_br.png`:  Number of Authors by Genders and Year (Book Reviews)
3. `gender_by_year_ra.png`: Number of Authors by Genders and Year (Research Articles)
4. `gender_proportion_year_all.png`: Gender Proportion of Authors by Year (All Articles)
5. `gender_proportion_year_br.png`: Gender Proportion of Authors by Year (Book Reviews)
6. `gender_proportion_year_ra.png`: Gender Proportion of Authors by Year (Research Articles)

### Unigram Analysis

The purpose of this analysis is to track the most popular significant words, by year, that appear in book reviews and research articles in *AJS Review*.  

For the unigram analysis, the first step was to separate the unigram files according to the type of article they summarize. This meant that book review unigram files were sorted into one directory and research article unigrams files into another. This was accomplished with the `data_separator` notebook. Please refer to the notebook for more details on this process.

A second script, `unigram_analysis.py`, was used to read all of the unigrams in each category (book review or research article) and to create new spreadsheets, `research-article_unigrams.csv` and `book-review_unigrams.csv` .  These files have taken all of the unigrams in each category, stripped out numbers that are not dates;  filtered out the stopwords provided by the NLTK package and our own file of stopwords.txt; and has sorted them by frequency.  We ran the script, manually examined the output identify additional stopwords that we added to the stopwords.txt file [how???], and repeated until we had a stopword list that we thought did a good job of filtering the noise from our data.

Methods Used

* To be decided...
*

### Analysis Process and Description of Contents

1. 
2. 

### Contributors
* Michael Satlow
* Alexander Berry
