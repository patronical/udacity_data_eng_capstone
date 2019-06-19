"""
Transforms the Tweets into numerical Sentiment scores.
Uses the Vader sentiment engine.
"""
from tqdm import tqdm_notebook
import got3
import pandas as pd
import os
import pickle
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def tweetSent(df_key):
    """
    Runs the clean text through the Sentiment Engine.
    Imports keword augmented dataframe.
    Returns a sentiment augmented dataframe.
    """
    print('1/3 sent_transformer, initializing.')

    df_sent = df_key.copy()
    root = 'proc_data'
    year = df_sent['date'][0].year
    month = df_sent['date'][0].month
    pos_list = []
    neu_list = []
    neg_list = []
    cmp_list = []
    analyzer = SentimentIntensityAnalyzer()

    print('2/3 sent_transformer, transforming tweets to sentiments.')

    for _,nrows in tqdm_notebook(df_sent.iterrows()):
        vs = analyzer.polarity_scores(nrows['cleantext'])
        pos_list.append(vs['pos'])
        neu_list.append(vs['neu'])
        neg_list.append(vs['neg'])
        cmp_list.append(vs['compound'])

    df_sent['vad_positive'] = pos_list
    df_sent['vad_neutral'] = neu_list
    df_sent['vad_negative'] = neg_list
    df_sent['vad_compound'] = cmp_list

    filename = 'proc_sent_{}_{}.pkl'.format(year,month)
    filestring = os.path.join(root, filename)

    # output to pickle
    with open(filestring, 'wb') as filehandle:  
        # store the data
        pickle.dump(df_sent, filehandle)

    print('3/3 sent_transformer, process complete.')
    return df_sent
