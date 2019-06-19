"""
Tokenizes the clean tweet text strings into individual words.
Filters out stopwords from tokens to create Keywords.
Uses natural language tool kit for processing.
"""
from tqdm import tqdm_notebook
import got3
import pandas as pd
import os
import pickle
import numpy as np
import re
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

def tokenKey(df_clean):
    """
    Renders clean text into tokens.
    Counts number of tokens.
    Strips stop words out of tokens to make keywords.
    Counts keywords.
    Pickles the results.
    Imports clean text dataframe.
    Returns augmented dataframe.
    """
    print('1/4 keyword_tokenizer, initializing.')

    df_token = df_clean.copy()
    root = 'proc_data'
    year = df_token['date'][0].year
    month = df_token['date'][0].month
    tok_list = []
    len_list = []
    bare_tok = []
    bare_cnt = []

    tknzr = TweetTokenizer()

    stoplist = list(set(stopwords.words('english'))) + \
            ['.',',','!','"','…','?','’',':','-','/',')',\
            '(','$','...','&','*',':)','%','”','“',"'",'+',';']

    print('2/3 keyword_tokenizer, keyword tokenizing.')

    for _,nrows in tqdm_notebook(df_token.iterrows()):

        # tokenize
        word_list = tknzr.tokenize(nrows['cleantext'])
        tok_list.append(word_list)
        len_list.append(len(word_list))

        # create keywords
        bare = []
        for Tok in word_list:
            tok = Tok.lower()
            if not (tok in stoplist):
                bare.append(tok)
        bare_set = list(set(bare))
        bare_tok.append(bare_set)
        bare_cnt.append(len(bare_set))

    # augment dataframe                
    df_token['tokens'] = tok_list
    df_token['tok_count'] = len_list
    df_token['keywords'] = bare_tok
    df_token['key_count'] = bare_cnt

    filename = 'proc_key_{}_{}.pkl'.format(year,month)
    filestring = os.path.join(root, filename)

    # pickle result
    with open(filestring, 'wb') as filehandle:  
        # store the data
        pickle.dump(df_token, filehandle)

    print('3/4 keyword_tokenizer, process complete.')
    return df_token
