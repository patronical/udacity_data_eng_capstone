"""
Cleans the raw tweet text.
Removes elements that likely cause sentiment noise.
"""
from tqdm import tqdm_notebook
import got3
import pandas as pd
import os
import pickle
import numpy as np
import re

def cleaner(text):
    """
    Imports raw tweet text.
    Cleans the text.
    Removes elements that likely cause sentiment noise.
    Returns clear clean tweet text.
    """
    # take out space after @ symbol
    clear = re.sub(r'@\s+',r'@', text)
    # take out usernames
    clear = re.sub(r'@([A-Za-z0-9_]+)','', clear)
    # take out space after # symbol
    clear = re.sub(r'#\s+',r'#', clear)
    # take out space after $ symbol
    clear = re.sub(r'$\s+',r'$', clear)
    # take out url
    clear = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','', clear) 
    # take out pics
    clear = re.sub(r'pic.twitter?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','', clear)
    # take out the extra white spaces
    clear = re.sub(r' +', ' ', clear.strip())
    return clear


def cleanTweets(df_lang):
    """
    Imports a language detected tweet dataframe.
    Runs each row's text through the washing machine.
    Sets an English language Flag.
    Pickles the update.
    Returns a dataframe.
    """

    print('1/3 tweet_cleaner, initializing.')

    df_eng = df_lang.copy()
    root = 'proc_data'
    year = df_eng['date'][0].year
    month = df_eng['date'][0].month
    english = []
    length = []
    cleantext = []

    print('2/3 tweet_cleaner, cleaning text.')

    for j,nrows in tqdm_notebook(df_eng.iterrows()):
        tag = 0
        if nrows['lang'] == 'en':
            tag = 1 
        clean = cleaner(nrows['text'])
        length.append(len(clean))
        cleantext.append(clean)
        english.append(tag)
    df_eng['english'] = english
    df_eng['length'] = length
    df_eng['cleantext'] = cleantext

    filename = 'proc_clean_{}_{}.pkl'.format(year,month)
    filestring = os.path.join(root, filename)

    # output to pickle
    with open(filestring, 'wb') as filehandle:  
        # store the data
        pickle.dump(df_eng, filehandle)

    print('3/3 tweet_cleaner, process complete.')
    return df_eng
