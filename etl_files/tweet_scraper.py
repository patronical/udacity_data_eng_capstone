"""
Extracts Tweets from Twitter.
Intended to update existing tweet collection.
"""

from tqdm import tqdm_notebook
import got3
import pandas as pd
import os
import pickle
import numpy as np

def getTweets(username, since, until):
    """
    Retrieves tweets from specific author and time span.
    Imports: username, date string since, date string until.
    Returns: dataframe of raw tweet info.
    """
    tweetCriteria = got3.manager.TweetCriteria().setUsername(username).setSince(since).setUntil(until).setMaxTweets(2000)
    tweets = got3.manager.TweetManager.getTweets(tweetCriteria)
    print(username, since, until)
    df_tweets = pd.DataFrame()  
    if len(tweets)>0:
        df_tweets['id'] = [i.id for i in tweets]
        df_tweets['date'] = [i.date for i in tweets]
        df_tweets['text']= [i.text for i in tweets]
        df_tweets['author'] = [username] * len(tweets)
        df_tweets['favorite'] = [i.favorites for i in tweets]
        df_tweets['url'] = [i.permalink for i in tweets]
    
    return df_tweets

def scrapeTweets():
    """
    Loads twitter screen_names.
    Loads times of interest.
    Extracts tweets.
    Pickles the results.
    Returns a dataframe of raw tweets.
    """
    print('1/3 tweet scraper, loading files.')

    with open('crypto_tweeter_seeds_060419.pkl', 'rb') as filehandle:  
        # read the data as binary data stream
        seeds = pickle.load(filehandle)

    df_time = pd.read_csv('scrape_time.csv')
    root = 'raw_data'
    years = df_time['year'].tolist()
    months = df_time['month'].tolist()

    print('2/3 tweet scraper, scraping tweets.')

    df_tweets = pd.DataFrame()
    for seed in tqdm_notebook(seeds):
        for year in years:
            for month in months:

                #load last version
                filename = 'raw_tweets_{}_{}.pkl'.format(year,month)
                filestring = os.path.join(root, filename)
                
                try:
                    with open(filestring, 'rb') as filehandle:  
                        # read the data as binary data stream
                        df_tweets = pickle.load(filehandle)
                except Exception as e:
                    print(e)
                    print('Starting with new dataframe.')
                    df_tweets = pd.DataFrame()

                #assign date range
                if month == 12:
                    since = "{}-{}-01".format(year,month)
                    until = "{}-{}-01".format(year+1, 1)
                else:
                    since = "{}-{}-01".format(year,month)
                    until = "{}-{}-01".format(year,month+1)
                try:    
                    df_add = getTweets(seed, since, until)
                    df_tweets = pd.concat([df_tweets, df_add], ignore_index=True)
                    df_tweets = df_tweets.drop_duplicates()
                except:
                    pass  #HTTP errors and Runtime errors seen in past
            
            # save update
            with open(filestring, 'wb') as filehandle:  
                # store the data
                pickle.dump(df_tweets, filehandle)

    print('3/3 tweet scraper, scraping complete.')
    return df_tweets   
