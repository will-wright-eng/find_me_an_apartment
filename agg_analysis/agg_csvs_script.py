import os
import sys
import datetime as dt

from io import StringIO 
from io import BytesIO

import boto3
import pandas as pd

import myconfigs

def main():
    today = str(dt.date.today())

    client = boto3.client('s3')
    bucket_name = myconfigs.bucket_name
    filelist = [e['Key'] for p in client.get_paginator("list_objects_v2")\
                             .paginate(Bucket=bucket_name)
              for e in p['Contents']][1:]

    dfs = []
    for key_name in filelist:
        print(key_name)
        s3_response_object = client.get_object(Bucket=bucket_name, Key=key_name)

        body = s3_response_object['Body']
        csv_string = body.read().decode('utf-8')

        df = pd.read_csv(StringIO(csv_string))
        dfs.append(df)
        
    ndf = pd.concat(dfs)
    # combine with historical data -- TODO add this csv to bucket
    # filename = myconfigs.filename
    # df = pd.read_csv(filename)
    # print(df.shape)
    # print(ndf.shape)
    # ndf = pd.concat([ndf,df])
    # print(ndf.shape)

    ndf.price = ndf.price.apply(lambda ele: float(ele.replace('$','').replace(',','')))
    ndf['where'] = ndf['where'].apply(lambda ele: str(ele).replace(',',''))
    ndf['where'] = ndf['where'].apply(lambda x: str(x).lower())
    no_cols = ['Unnamed: 0','available','address','geotag'] # columns that mess up the csv
    ndf = ndf[[i for i in list(ndf) if i not in no_cols]]
    ndf.to_csv(today+'_compiled_clist_results.csv',index=False)

if __name__ == '__main__':
    main()