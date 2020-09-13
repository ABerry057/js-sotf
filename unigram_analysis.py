import pandas as pd
from tqdm import tqdm
import re
import os
from pathlib import Path

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk_stopwords = stopwords.words('english')

base_dir = Path(os.getcwd()).resolve()  # get base dir
unigram_dir = base_dir / 'ngram1'  # get path to ngram1 subdir


def make_unigram_table(atype, a_ids=None):
    """Makes a dataframe by concatenating all unigrams from
        articles specified by a_ids.

    Arguments:
        atype {String} -- the article type to source unigrams
                          from: 'book-review', 'research-article',
                          or 'both'.

    Keyword Arguments:
        a_id {List} -- List of article IDs to include, by default
                       all articles are included. (default: {None})
    """
    if atype == "both":
        raise ValueError("Feature not yet supported!\n")
    curr_path = unigram_dir / atype
    # print(curr_path)
    dfs = []
    for f in tqdm(curr_path.iterdir()):
        f_id = re.search(f"{atype}/(.*)-n", str(f)).group(1)
        if a_ids is not None:
            if f_id in a_ids:
                # print("Match!")  # for debugging
                unigrams = pd.read_csv(f, sep='\t', names=["word", "count"])
                # print(f"Just read {f_id}")  # for debugging
                dfs.append(unigrams)
            else:
                # print(f"{f_id} not in a_ids list")
                continue
        else:
            unigrams = pd.read_csv(f, sep='\t', names=["word", "count"])
            # print(f"Just read {f_id}")  # for debugging
            dfs.append(unigrams)
    print(f"\nCollected {len(dfs)} articles\n")
    if not dfs:
        raise ValueError("Unable to collect dataframes")
    concat_df = pd.concat(dfs)
    summed_df = concat_df.groupby(["word"]).sum().reset_index()
    sorted_df = summed_df.sort_values(by=["count"], ascending=False)
    return sorted_df


def lemmatize_table(df):
    """Lemmatizes the words in the word column of an ngram table. Sums
       frequencies of words that map to the same lemma.

    Arguments:
        df {Pandas dataframe} -- ngram table with columns 'word' and 'count'.
    """
    if df is None:
        print("The passed object is of None type")
        return "Error"
    lemmatizer = WordNetLemmatizer()

    def lemmatize_word(word):
        """Uses lemmatization from spacy to map words to lemmas.
           (Could do with some tweaking to better group lemmas).

        Arguments:
            word {String} -- lowercase word to lemmatize

        Returns:
            String -- lemmatized word
        """
        return lemmatizer.lemmatize(word)
    df_lemma = df.copy()
    df_lemma['word'] = df['word'].map(lemmatize_word, na_action="ignore")
    summed_df = df_lemma.groupby(["word"]).sum().reset_index()
    sorted_df = summed_df.sort_values(by=["count"], ascending=False)
    return sorted_df


def make_custom_stopword_list(df):
    """Creates and saves a custom stopword list as a plain text file in the data directory.

    Arguments:
        df {Pandas Dataframe} -- A dataframe of with columns 'word', 'count', 'stopword'
        which is a table of ngram frequencies that has been manually labeled with an 'x'
        to indicate inclusion. Words marked with 'r' have already been reviewed and will
        not be added to the stop list. All other words are added to the stop list.
    """
    stopwords = []
    for i, row in tqdm(df.iterrows(), desc="Creating stopwords\n"):
        stopword_status = row['stopword']
        if stopword_status == 'r': # if 'r', word has already been reviewed, so ignore
            continue
        if stopword_status == 'x': # if 'x', word is marked for inclusion, so ignore
            df.loc[i,'stopword'] = 'r' # update 'x' to 'r'
        if stopword_status == "unchecked": # if 'unchecked', wait for manual review
            continue
        else:
            stopwords.append(row['word'])
    with open("custom_stopwords.txt", "w+") as filehandle:
        for word in stopwords:
            filehandle.write(f"{word}\n")


def is_year(string):
    """Returns a boolean value if the input string likely represents a year.
       Only valid for years 1000-2999.
    Arguments:
        string {String} -- candidate string
    """
    return bool(re.match("(1|2)\d{3}", string))


def remove_numerals(df, remove_mixed_strings=True):
    """Removes rows from an ngram table with words that are numerals. This
       does not include 4-digit numbers which are interpreted as years.

    Arguments:
        df {Pandas dataframe} -- A dataframe of with columns 'word', 'count'.

    Keyword Arguments:
        remove_mixed_strings {bool} -- Whether to remove rows with words that
        are mixtures of numerals and letters. (default: {True})
    """
    no_numerals_df = df.copy().reset_index()
    for i, row in tqdm(no_numerals_df.iterrows(), desc="Removing numerals\n"):
        word = row['word']
        if remove_mixed_strings:
            if any([c.isnumeric() for c in word]) and \
               not is_year(word):
                no_numerals_df.drop(i, axis=0, inplace=True)
        else:
            if word.isnumeric() and len(word) != 4:
                no_numerals_df.drop(i, axis=0, inplace=True)
    return no_numerals_df


def remove_stopwords(df, include_custom=False):
    """Removes rows from an ngram table with words
       in a custom stopword list or in NLTK list.

    Arguments:
        df {Pandas dataframe} -- ngram table with columns "word" and "stopword"
    """
    with open("custom_stopwords.txt") as f:
        custom_stop = f.readlines()
    custom_stop = [w.strip() for w in custom_stop]
    no_stops_df = df.copy()
    for i, row in tqdm(no_stops_df.iterrows(), desc="Removing stopwords\n"):
        word = row['word']
        if include_custom:
            if word in nltk_stopwords or word in custom_stop:
                no_stops_df.drop(i, axis=0, inplace=True)
        else:
            if word in nltk_stopwords:
                no_stops_df.drop(i, axis=0, inplace=True)
    return no_stops_df


def drop_counts(df, threshold):
    """Removes rows from an ngram table with counts fewer than threshold.

    Arguments:
        df {Pandas dataframe} -- ngram table with columns "word" and "count"
        threshold {Integer} -- minimum count to keep rows
    """
    dropped_df = df[df['count'] >= threshold]
    return dropped_df
