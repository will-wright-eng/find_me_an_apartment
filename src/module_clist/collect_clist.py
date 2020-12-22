'''
craigslist module

Author: William Wright
'''

import pandas as pd
import datetime as dt

def search_to_df():
    '''docstring for search_craigslist'''
    csv_filename = '_craigslist_app_search_results.csv'
    cl_h = CraigslistHousing(site='sfbay',
                             area='sfc',
                             filters={
                                 'min_price': 4000,
                                 'max_price': 7500,
                                 'search_distance': 4,
                                 'zip_code': 94133,
                                 'min_bedrooms': 3,
                                 'max_bedrooms': 3
                             })

    i = 0
    dfs = []
    # print('parsing results')
    for result in cl_h.get_results(sort_by='newest',
                                   geotagged=True,
                                   include_details=True):
        temp = pd.DataFrame(list(result.items())).T
        cols = list(temp.iloc[0])
        temp.columns = cols
        temp = temp.iloc[-1]
        temp = pd.DataFrame(temp).T
        dfs.append(temp)
        i = i + 1

    # print(str(i + 1) + ' listings collected')
    df = pd.concat(dfs, sort=False)
    df['script_timestamp'] = dt.datetime.now()
    return df

def clean_clist_df(df):
    '''docstring for clean_craigslist_df'''
    
    # df = df.sort_values(by='script_timestamp', ascending=True)
    df = df.infer_objects()
    df = df[[i for i in list(df) if 'Unnamed' not in i]]
    
    # df['date_available'] = pd.to_datetime(df['date_available'])
    df['bedrooms'] = df['bedrooms'].astype(int,errors='ignore')
    
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
    temp.columns = ['cols','col_dtype']
    temp = temp.loc[temp.col_dtype=='object']
    for col in list(temp.cols):
        df[col] = df[col].astype(str)    

    df.reset_index(inplace=True,drop=True)

    return df