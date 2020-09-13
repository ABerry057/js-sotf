import pandas as pd
from tqdm import tqdm
from pathlib import Path
from unigram_analysis import *
import plotly.express as px

file_path = Path(__file__).resolve()  # get path of this file
base_dir = file_path.parents[0]  # get path of parent directory
unigram_dir = base_dir / 'ngram1'  # get path to ngram1 subdir
figure_dir = base_dir / 'figures'


def unigram_by_years(years, atype, reference_df):
    """Given a range of years, returns a dataframe of unigrams and
       associated counts from articles from those years

    Arguments:
        years {Range} -- For AJS data set, valid ranges of years
        are between 1980 and 2014.

        atype {String} -- 'research-article' or 'book-review'

        reference_df {Pandas Dataframe} -- a dataframe with
        'id' and 'year' columns.
    """
    a_ids = []
    for year in years:
        ids = reference_df.loc[(reference_df['year'] == year) & (reference_df['type'] == atype)]['id'].values.tolist()
        a_ids += ids
    if a_ids == []:
        raise ValueError("No articles for given range")
    # a_ids = [id for sublist in a_ids for id in sublist]  # flatten list of lists into 1D
    # print(f"a_ids is: {a_ids}")  # for debugging
    raw_table = make_unigram_table(atype, a_ids)
    lemmatized = lemmatize_table(raw_table)
    no_num = remove_numerals(lemmatized)
    no_stops = remove_stopwords(no_num, True)
    return no_stops


def stringify_span(range):
    """Returns a nicely-formatted string representing a span of years.

    Arguments:
        range {range} - A range object
    """
    if len(range) >= 2:
        timespan = f"{range[0]}-{range[-1]}"
    else:
        timespan = range[0]
    return timespan


def make_top_unigram_chart(reference_df, n, years, atype, plot_lib='px'):
    """Makes a barchart showing the top n most common unigrams
       from unigram_df.

    Arguments:
        reference_df {Pandas Dataframe} -- a dataframe with
        'id' and 'year' columns.
        n {Integer} -- number of unigrams to include in the chart
        years {Integer} -- Range of years to include in chart title. 
        For AJS data set, valid years are 1980 - 2014.
        atype {String} -- 'research-article' or 'book-review' to
        include in chart title
    Keyword Arguments:
        plot_lib {String} -- plotting library to use, valid choices
        are 'px' and 'sns'. By default, 'px'
    """
    unigram_df = unigram_by_years(years, atype, reference_df)
    if atype == "book-review":
        atype = "Book Reviews"
    elif atype == "research-article":
        atype = "Research Articles"
    timespan = stringify_span(years)
    top_n = unigram_df.nlargest(n, "count").sort_values(by='count', ascending=True)
    fig = px.bar(top_n, x="count", y="word", text="count", orientation="h",
                 color_discrete_sequence=["black"],
                 title=f"Top {n} Unigram Counts from AJS {atype}: {timespan}",
                 labels={"count": "Count",
                            "word": "Word"
                            }
                    )
    fig.update_xaxes(showticklabels=False)
    fig.update_traces(textposition='outside')
    fig.update_layout(uniformtext_minsize=24,
                      uniformtext_mode='hide',
                      margin=dict(l=20, r=20, t=40, b=20))
    fig.layout.template = "plotly_white"
    return fig
