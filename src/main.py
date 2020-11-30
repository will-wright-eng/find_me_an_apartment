'''
config.py
# config.password # password string
# config.myemail # email string
# config.recipients # list of strings
# config.recipients_test # single element list (which is a string)

Author: William Wright
'''

import os
import glob
import sys
import pandas as pd
import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import smtplib

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.message import Message
from email.mime.text import MIMEText
from email import encoders

from craigslist import CraigslistHousing

import config
from search_cl import search_craigslist
from send_email import mail


def clean_craigslist_df(df):
    '''docstring for clean_craigslist_df'''
    df = df.sort_values(by='script_timestamp', ascending=True)
    df = df[[i for i in list(df) if 'Unnamed' not in i]]
    # geotag split
    df['geotag_lat'] = df['geotag'].apply(lambda x: str(x).split(',')[0])
    df['geotag_lat'] = df['geotag_lat'].apply(lambda x: x.replace('(', ''))
    df['geotag_lon'] = df['geotag'].apply(lambda x: str(x).split(',')[1])
    df['geotag_lon'] = df['geotag_lon'].apply(lambda x: x.replace(')', ''))
    # commas fucking with Tableau import
    df['name'] = [i.replace(',', '') for i in list(df['name'])]
    # Tableau not reading date properly
    df['date_posted'] = pd.to_datetime(df['datetime']).dt.date
    df['date_last_updated'] = pd.to_datetime(df['last_updated']).dt.date
    df['date_script_timestamp'] = pd.to_datetime(
        df['script_timestamp']).dt.date
    df['date_available'] = pd.to_datetime(df['available'] + ' 2020').dt.date
    df['days_till_available'] = df['date_available'].apply(
        lambda x: pd.to_datetime(x) - pd.to_datetime(dt.date.today()))
    return df

def make_bar_chart(df, col, title_append=''):
    '''docstring for make_bar_chart'''
    ndf = pd.DataFrame(
        df[col].value_counts()).reset_index().sort_values(by='index')
    ndf = ndf.set_index('index')
    ndf.plot(kind='bar', figsize=(10, 4))
    plt.xticks(rotation=90)
    plt.title('number of listings by ' + col + ' [' + title_append + ']')
    plt.tight_layout()

    today = str(dt.date.today())
    if len(title_append) > 0:
        title_append = title_append.replace(' ', '_')
        filename = today + '_count_listings_by_' + col + '_' + title_append + '.png'
    else:
        filename = today + '_count_listings_by_' + col + '.png'
    path = cwd + '/images'
    os.chdir(path)
    plt.savefig(filename, dpi=300)
    os.chdir(cwd)
    return filename

def combine_craigslist_csvs():
    '''docstring for combine_craigslist_csvs'''
    path = cwd + '/csvs'
    os.chdir(path)

    extension = 'csv'
    result = glob.glob('*.{}'.format(extension))
    csvs = [i for i in result if 'craigslist' in i]
    dfs = []
    for csv in csvs:
        dfs.append(pd.read_csv(csv))

    df = pd.concat(dfs, sort=False)
    # sort such that the most recent script instance is at the bottom
    df = df.sort_values(by='script_timestamp', ascending=True)
    # print('concat csvs \t= ', len(df), ' rows')

    # keep only the last instance so that the most recent script timestamp is kept
    # datediff between listing and last timestamp can act as a proxy for post longevity
    df = df.drop_duplicates(subset='id', keep='last')
    # print('deduped df \t= ', len(df), ' rows')
    df['date_script_timestamp'] = pd.to_datetime(
        df['script_timestamp']).dt.date
    df['currently_listed'] = df['date_script_timestamp'].apply(
        lambda x: dt.date.today() == x)

    today = str(dt.date.today())
    csv_filename = today + '_compiled_search_results.csv'
    df = clean_craigslist_df(df)

    # print('saving file...')
    df.to_csv(csv_filename, index=False)
    os.chdir(cwd)
    # print('saved successfully')
    make_bar_chart(df, 'date_available', 'combined csv')

def main():
    '''docstring for main'''
    cwd = os.getcwd()
    input1 = input('Testing python script? (y/n/m)\n')
    if input1 == 'y':
        # print('\ntesting...')
        recipients = config.recipients_test
    elif input1 == 'n':
        # print('\nfull email list used')
        recipients = config.recipients
    elif input1 == 'm':
        # print('\ncontacting the messiah of entropy')
        recipients = config.meena
    else:
        print('\nnot a valid answer')
        sys.exit()

    # print('\n', '-' * 6, 'run search')
    search_result_filenames, new_posts = search_craigslist()
    # print('\n', '-' * 6, 'run csv aggregator')
    combine_craigslist_csvs()

    # print('\n', '-' * 6, 'send email')
    today = str(dt.date.today())
    to = recipients
    subject = today + " Craigslist Search Results"
    text = new_posts + \
        ' \n\n\n\nCraigslist search parameters: \n \
        https://sfbay.craigslist.org/search/sfc/apa?search_distance=4&postal=94133&min_price=4000&max_price=7500&min_bedrooms=3&availabilityMode=0&sale_date=all+dates \
        \nCode: \n https://github.com/william-cass-wright/find_me_an_apartment/tree/master'
    attach = search_result_filenames
    mail(to, subject, text, attach)
    # print(text, '\n')


if __name__ == '__main__':
    main()
    # print('program successful!\n')
