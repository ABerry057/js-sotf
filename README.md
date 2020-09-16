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

The website can be seen [here](http://www.jewishstudies.digitalscholarship.brown.edu/).

### Data

Our original plan was to "plug and play" with the scripts that Andrew Goldstone used for his [topic modelling of the *PMLA*](https://agoldst.github.io/dfr-browser/demo/).  This project is based on the [JSTOR Data for Research service](https://www.jstor.org/dfr/) (DfR).  It turns out that since the development of that set of scripts, DfR has changed the way in which they deliver their data, so we found, modified, and created several scripts (all found in this repository) that work with DfR data as it is currently (May, 2020) delivered.

We requested the full data for the full run of *AJS Review*.  This required filling out a form and then agreeing to certain licensing restrictions for the data (e.g., we cannot redistribute it).  Once we agreed, we were sent a link to download a zipped file.  When extracted, the file unpacks into five folders: metadata; ngram1; ngram2; ngram3; and ocr.  The metadata folder contains XML files; the others are text files.  The names of all the files are, fortunately, identical other than their extension or ending (e.g., journal-article-10.2307.1486231.xml; journal-article-10.2307.1486231.ngram1.txt; journal-article-10.2307.1486231.txt).  All the files that share a particular id are a single research article, book review, or something else (called "miscellaneous," e.g., front matter) - the metadata xml files helpfully indicates which of these three types it is.  

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

A second notebook, `data_cleaning`, was used to read all of the unigrams in each category (book review or research article), strip numbers that are not dates, filter out the stopwords provided by the NLTK package and our own file of stopwords.txt, and sort unigrams by frequency.  We ran the notebook, manually examined the output, identified additional stopwords that we then added to the `custom_stopwords.txt` file, and repeated until we had a stopword list that we thought did a good job of filtering the noise from our data.

To visualize the unigrams with sparklines, we used the `sparklines` notebook. Given an article type, time period, bin size, and the number of words to use, it creates a sparkline visualization showing the changes in unigram frequency. The visualization is quite simple and is created with matplotlib, which allows for extensive customization of the visualization.

### Topic Modeling

Topic modeling begins with a dataframe that contains the texts of the article.  The general strategy, in `DfRModeling`, is (1) to clean the text and put it in a form that can be modeled; (2) to determine the best number of topics to use and the best number of passes; (3) to chose a particular model and assign topics to it; and (4) to produce the files needed to visualize the topics through time.

Once you determine the best number of topics and passes, `Topic Files Bulk Processing` can be used to run the models (assuming you want the same number of topics and passes for each) on multiple chunks of date ranges and types of articles.  You might, for example, want to create pyLDAvis files for research articles in five year chunks.



### Citation Network

The citation network analysis began with using the `csv_creation` notebook's secondary output, a CSV file of citations sourced from the original XML metadata files. To create CSV files for both nodes and edges, we used the `citation_network` notebook. The detailed process, which involves some manual cleaning and formatting, is documented in the notebook itself. The final result is two files: `nodes.csv` and `edges.csv`.

To build a network and visualize it, we used the `network_visualization` notebook. This will generate a static rendering of the network and two optional, additional visualizations. The visualization code has many options to tweak the resulting network, including node size, node color, network layout, and more. The processed node and edge data can also be used as input to other visualization tools such as Gephi.

### Contributors
* Michael Satlow
* Alexander Berry
