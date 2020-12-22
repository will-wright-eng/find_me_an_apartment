'''
Author: William Wright
'''

import os
import datetime as dt
import pandas as pd
import logging
import inspect

from craigslist import CraigslistHousing
import module_utils.function_logger as fl
import module_clist.collect_clist as search_cl
import module_utils.s3_funks as s3_funks

today = str(dt.date.today())
logger = fl.function_logger(logging.DEBUG, logging.DEBUG, function_name='test_dag')

def collect_clist_data():
    cl_h = CraigslistHousing(site='sfbay',
                             area='sfc',
                             filters={
                                 'min_price': 1000,
                                 'max_price': 6000,
                                 'search_distance': 4,
                                 'zip_code': 94133,
                                 'posted_today': True
                             })

    i = 0
    dfs = []
    logger.info('parsing results')
    for result in cl_h.get_results(sort_by='newest',
                                   geotagged=True,
                                   include_details=True):
        logger.info('get results for row '+str(i))
        temp = pd.DataFrame(list(result.items())).T
        cols = list(temp.iloc[0])
        temp.columns = cols
        temp = temp.iloc[-1]
        temp = pd.DataFrame(temp).T
        dfs.append(temp)
        i = i + 1

    logger.info(str(i + 1) + ' listings collected')
    df = pd.concat(dfs, sort=False)
    df['script_timestamp'] = dt.datetime.now()

    ndf = search_cl.clean_clist_df(df)
    return ndf

def main():
    '''docstring for main'''
    df = collect_clist_data()

    # folder = 'results'
    # try:    
    #     os.mkdir(folder)
    # except FileExistsError as e:
    #     logger.warning(e)

    filename = today+'_clistings.csv'
    # df.to_csv(folder+'/'+filename,index=False)
    keyname = "craigslist-tables/"+filename
    bucket = "project-rac"
    # s3_funks.write_csv_to_s3(df, bucket, keyname, folder+'/'+filename)
    s3_funks.write_df_to_s3(df, bucket, keyname)
    # s3_funks.write_pandas_parquet_to_s3(df, bucket, keyname, filename)
    # df.to_parquet(folder+'/'+filename,index=False)

if __name__ == '__main__':
    main()
    logger.info('program successful!\n')
