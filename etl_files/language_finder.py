"""
Detects the language of the raw tweet text.
Uses multiprocessing to avoid days of detection time.
Uses Google language detect algo via langdet script for mp use.
"""
from tqdm import tqdm_notebook
import got3
import pandas as pd
import os
import pickle
import numpy as np
import langdet
import multiprocessing as mp

def detectLang(df_raw):
    """
    Detects tweet language.
    Imports raw dataframe.
    Senses language of text on each row.
    Creates language label tag.
    Imports dataframe of raw tweets.
    Returns dataframe with language tag field.
    """

    print('1/3 language_finder, initializing.')

    df_proc = df_raw.copy()
    root = 'proc_data'
    year = df_proc['date'][0].year
    month = df_proc['date'][0].month

    # create the multiprocessing pool
    cores=mp.cpu_count()
    pool = mp.Pool(cores)

    print('2/3 language_finder, detecting language.')
    # process the tweet text
    with mp.Pool(cores) as pool:
        result = pool.map(langdet.langfind, df_proc['text'].iteritems())

    # close down the pool
    pool.close()
    
    # write result to column
    df_proc['lang'] = result
    
    filename = 'proc_lang_{}_{}.pkl'.format(year,month)
    filestring = os.path.join(root, filename)
    
    # output to pickle
    with open(filestring, 'wb') as filehandle:  
        # store the data
        pickle.dump(df_proc, filehandle)
    
    print('3/3 language_finder, process complete.')
    return df_proc
