import pandas as pd
import re
from tqdm import tqdm
import xml.etree.ElementTree as ET
from pathlib import Path


def get_citations(doc_type, citation_cols, doc_id, doc_title, doc_author, doc_root):
    if doc_type != 'research-article':
        return pd.DataFrame()
    xml_cits = doc_root.findall('back/fn-group/fn/p/mixed-citation')
    citation_block = {}
    for i in range(len(xml_cits)):
        try:
            cit_author = xml_cits[i].find('person-group/string-name/surname').text
        except AttributeError:
            cit_author = ''
        try:
            cit_title = xml_cits[i].find('source').text
        except AttributeError:
            cit_title = ''
        try:
            cit_year = xml_cits[i].find('year').text
        except AttributeError:
            cit_year = ''
        try:
            cit_reference = xml_cits[i].text
        except AttributeError:
            cit_reference = ''
        citation = (doc_id, doc_title, doc_author, cit_author, cit_title, cit_year, cit_reference)
        citation_block[i] = citation
    block_df = pd.DataFrame.from_dict(citation_block, columns=citation_cols, orient='index')
    return block_df


def xml2csv(src_path):
    """Creates an initial dataset from XML files found in src_path. Columns of the data CSV include
    id, author, title, year, type, and language. Columns of the citations CSV include
    id, article author, title, year, source, and a general citation. Returns a tuple of Pandas dataframes.

    Args:
        src_path (String): path to directory of XML files to pull metadata from
    """
    src_path = Path(src_path).resolve()
    files = src_path.iterdir()

    data_cols = ['id', 'type', 'title', 'auth1', 'year', 'lang']
    data_df = pd.DataFrame(columns=data_cols)

    citations_cols = ['id', 'title', 'article_author', 'citation_author',
                        'citation_source', 'citation_year', 'citation_general']
    citations_df = pd.DataFrame(columns=citations_cols)
    citation_blocks = {}

    for i, f in tqdm(enumerate(files), desc='Reading metadata files'):
        tree = ET.parse(f)
        root = tree.getroot()
        id = str(f).split("metadata/")[1].split(".x")[0]
        type = root.attrib['article-type']
        # title handling
        title_group = root.find('front/article-meta/title-group')
        if title_group is not None and len(title_group.getchildren()) > 0:
            title = list(title_group.itertext())[1]
        else:
            title = ''
        # author handling
        contrib_group = root.find('front/article-meta/contrib-group')
        if contrib_group is not None and len(contrib_group.getchildren()) > 0:
            auth1 = ' '.join([list(c.itertext())[0] for c in root.find('front/article-meta/contrib-group/contrib/string-name')])
        else:
            auth1 = ''
        lang = list(root.find('front/article-meta/custom-meta-group/custom-meta/meta-value').itertext())[0]
        year = int(list(root.find('front/article-meta/pub-date/year').itertext())[0])
        data_df.loc[i] = [id, type, title, auth1, year, lang]
        citation_blocks[i] = get_citations(type, citations_cols, id, title, auth1, root)

    citations_df = pd.concat([citations_df] + list(citation_blocks.values()))
    print(f"\nCollected {data_df.shape[0]} articles")
    return (data_df, citations_df)


# clean auth1 values by splitting merged names
def format_names(name):
    """Splits merged strings representing author names into forename and surname.
    Does not modify correctly formatted names.

    Arguments:
        name {String} -- Merged fore and surnames
    """
    n_caps = len(re.findall('[A-Z]', name))
    n_spaces = len(re.findall(' ', name))
    if any("\u0590" <= c <= "\u05EA" for c in name):
        # pass formatting for non-English names
        return name
    if n_caps - n_spaces != 1:
        comps = re.findall('[A-Z][^A-Z]*', name)
        # remove whitespace before or after components
        comps = [c.strip() for c in comps]
        f_name = " ".join(comps).replace("- ", "-").replace("I ", "I")
        return f_name
    else:
        return name


def remove_misc_articles(df):
    """Removes articles with the type 'misc' and stores them in a
    separate dataframe. Returns a tuple of the misc dataframe
    and a copy of df with the misc article rows removed.

    Args:
        df (Pandas dataframe): Dataframe from which to remove misc rows

    Returns:
        [Tuple]: (misc dataframe, copy of original dataframe with misc removed)
    """
    clean_df = df.copy()
    misc_indices = df[df['type'] == 'misc'].index
    misc_df = df.loc[misc_indices]
    clean_df.drop(misc_indices, axis=0, inplace=True)
    return (clean_df, misc_df)
