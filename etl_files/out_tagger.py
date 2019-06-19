"""
Tag entries for the purpose of excluding outliers.
Utilizes insights gained from development analytic studies.
Marks 1's for okay state, 0's for not okay state.
Intended for use as filtering down noise in sentiment.
"""
from tqdm import tqdm_notebook
import pandas as pd
import os
import pickle

def tagOkay(df_sent):
    """
    Checks row parameters against quality criterions.
    Tags row with corresponding result.
    Imports sentiment scored dataframe.
    Pickles the result.
    Outputs tag augmented dataframe.
    """
    print('1/3 out_tagger, initializing.')

    df_tag = df_sent.copy()
    root = 'proc_data'
    year = df_tag['date'][0].year
    month = df_tag['date'][0].month
    poet_ok = []
    tweet_ok = []
    sent_ok = []
    keyword_ok = []

    # load selected poets - found in analytics worksheet
    with open('screened_seeds_06119.pkl', 'rb') as filehandle:  
        # store the data as binary data stream
        selected = pickle.load(filehandle)

    # context checked against lower case keywords
    context = ['bitcoin', '#bitcoin', 'btc', 'bitcoins']   


    print('2/3 out_tagger, tagging data.')

    for _,nrows in tqdm_notebook(df_tag.iterrows()):

        # check poet
        p_flag = 0
        if nrows['author'] in selected:
            p_flag = 1
        
        #check tweet isn't short
        t_flag = 0
        if nrows['key_count'] > 3:
            t_flag = 1
        
        #check sentiment seems legit
        s_flag = 0
        if ((nrows['vad_compound']!=0)&(nrows['vad_neutral']!=1)):
            s_flag = 1
        
        #check keywords
        k_flag = 0
        hits = [k for k in nrows['keywords'] if k in context]
        if len(hits)>0:
            k_flag = 1
        
        poet_ok.append(p_flag)
        tweet_ok.append(t_flag)
        sent_ok.append(s_flag)
        keyword_ok.append(k_flag)

    df_tag['poet_ok'] = poet_ok
    df_tag['tweet_ok'] = tweet_ok
    df_tag['sent_ok'] = sent_ok
    df_tag['key_ok'] = keyword_ok

    filename = 'proc_tweets_{}_{}.pkl'.format(year,month)
    filestring = os.path.join(root, filename)

    # output to pickle
    with open(filestring, 'wb') as filehandle:  
        # store the data
        pickle.dump(df_tag, filehandle)

    print('3/3 out_tagger, process complete.')
    return df_tag

