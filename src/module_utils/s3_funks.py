'''Author: William Wright'''

import boto3
from io import BytesIO


def get_parquet_from_s3(bucket, keyname):
    '''get_parquet_from_s3 docstring'''
    s3 = boto3.client('s3')
    s3_response_object = s3.get_object(Bucket=bucket, Key=keyname)
    df = s3_response_object['Body'].read()
    df = pd.read_parquet(BytesIO(df))
    return df


def write_pandas_parquet_to_s3(df, bucketname, keyname):
    s3_url = 's3://' + bucketname + '/' + keyname
    df.to_parquet(s3_url, compression='gzip')
    return print('done')


def write_csv_to_s3(df, bucketname, keyname, filename):
    # instantiate S3 client and upload to s3
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(filename, bucketname, keyname)


def write_df_to_s3(df, bucket, keyname):
    from io import StringIO  # python3 (or BytesIO for python2)

    csv_buffer = StringIO()
    df.to_csv(csv_buffer)

    s3 = boto3.resource('s3')
    s3.Object(bucket, keyname).put(Body=csv_buffer.getvalue())
