'''
craigslist module

Author: William Wright
'''

import pandas as pd
import datetime as dt


def clean_clist_df(df):
    '''docstring for clean_craigslist_df'''

    df = df.infer_objects()
    df = df[[i for i in list(df) if 'Unnamed' not in i]]
    df['bedrooms'] = df['bedrooms'].astype(int, errors='ignore')

    # geotag split
    df['geotag_lat'] = df['geotag'].apply(lambda x: str(x).split(',')[0])
    df['geotag_lat'] = df['geotag_lat'].apply(lambda x: x.replace('(', ''))
    df['geotag_lon'] = df['geotag'].apply(lambda x: str(x).split(',')[1])
    df['geotag_lon'] = df['geotag_lon'].apply(lambda x: x.replace(')', ''))

    # commas fucking with Tableau import
    df['name'] = [i.replace(',', '') for i in list(df['name'])]

    # Tableau not reading dates properly
    cols_date = [i for i in list(df) if 'date' in i]
    for col in cols_date:
        df[col] = pd.to_datetime(df[col]).dt.date
    df['date_available'] = pd.to_datetime(df['available'] + ' 2020').dt.date
    df['days_till_available'] = df['date_available'].apply(
        lambda x: pd.to_datetime(x) - pd.to_datetime(dt.date.today()))

    temp = pd.DataFrame(df.dtypes).reset_index()
    temp.columns = ['cols', 'col_dtype']
    temp = temp.loc[temp.col_dtype == 'object']
    for col in list(temp.cols):
        df[col] = df[col].astype(str)

    df.reset_index(inplace=True, drop=True)

    return df
