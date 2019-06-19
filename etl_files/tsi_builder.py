"""
Builds Twitter Sentiment Indicator (TSI).
Based on Vader Compound sentiment scores.
Utilizes filtered version of processed data.
Intended to update existing indicator.
"""
import pandas as pd
import os

def loadInd(df_tag, old_csv_file):
    """
    Builds the TSI indicator.
    Imports tagged tweet dataframe.
    Imports old TSI csv filename.
    Loads update into new csv file.
    Returns updated TSI.
    """

    print('1/3 tsi_builder, initializing.')

    df_pro = df_tag.copy()
    year = max(df_pro['date']).year
    month = max(df_pro['date']).month
    day = max(df_pro['date']).day

    df_old = pd.read_csv(old_csv_file)
    df_old['date'] = pd.to_datetime(df_old.date, format="%Y-%m-%d")

    print('2/3 tsi_builder, building indicator.')

    # slice using the filters
    df_slice = df_pro[(df_pro['poet_ok']==1)&(df_pro['tweet_ok']==1)\
                      &(df_pro['sent_ok']==1)&(df_pro['key_ok']==1)].copy()

    # index subset
    df_new = df_slice[['date','vad_compound']].copy()

    #sort dates ascending
    df_new = df_new.sort_values('date')

    #aggregate by days
    df_3 = df_new.set_index('date').groupby(pd.Grouper(freq='D')).mean()
    df_3 = df_3.reset_index()

    #merge with the old
    cutover = df_old.index[df_old['date']==df_3['date'][0]].values[0]
    df_ind = pd.concat([df_old[0:cutover], df_3], ignore_index=True)

    #copy to csv
    df_ind.to_csv('tsi_{}_{}_{}.csv'.format(month,day,year),index=False)

    print('file created: '+'tsi_{}_{}_{}.csv'.format(month,day,year))

    print('3/3 tsi_builder, process complete.')
    return df_ind
