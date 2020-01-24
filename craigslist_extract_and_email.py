# https://pypi.org/project/python-craigslist/
# https://github.com/juliomalegria/python-craigslist/blob/master/craigslist/craigslist.py
# https://github.com/juliomalegria/python-craigslist/blob/master/craigslist/base.py

# https://pypi.org/project/python-craigslist/
# https://github.com/juliomalegria/python-craigslist/blob/master/craigslist/craigslist.py
# https://github.com/juliomalegria/python-craigslist/blob/master/craigslist/base.py

# create two folders in directory: images & csvs
# this will keep your saved files neatly organized

import os
import glob

import pandas as pd
from craigslist import CraigslistHousing
import datetime as dt

import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.message import Message
from email.mime.text import MIMEText
from email import encoders

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

# import credentials from separate file
import config
# config.password # password string
# config.myemail # email string
# config.recipients # list of strings

cwd = os.getcwd()

###

def clean_craigslist_df(df):
    df = df.sort_values(by='script_timestamp',ascending=True)
    df = df[[i for i in list(df) if 'Unnamed' not in i]]
    ###
    # geotag split
    df['geotag_lat'] = df['geotag'].apply(lambda x: str(x).split(',')[0])
    df['geotag_lat'] = df['geotag_lat'].apply(lambda x: x.replace('(',''))
    df['geotag_lon'] = df['geotag'].apply(lambda x: str(x).split(',')[1])
    df['geotag_lon'] = df['geotag_lon'].apply(lambda x: x.replace(')',''))
    # commas fucking with Tableau import
    df['name'] = [i.replace(',','') for i in list(df['name'])]
    # Tableau not reading date properly
    df['date_posted'] = pd.to_datetime(df['datetime']).dt.date
    df['date_last_updated'] = pd.to_datetime(df['last_updated']).dt.date
    df['date_script_timestamp'] = pd.to_datetime(df['script_timestamp']).dt.date
    df['date_available'] = pd.to_datetime(df['available']+' 2020').dt.date
    df['days_till_available'] = df['date_available'].apply(lambda x: pd.to_datetime(x) - pd.to_datetime(dt.date.today()))
    #df['currently_listed'] = df['date_script_timestamp'].apply(lambda x: dt.date.today()==x)
    return df
###

def make_bar_chart(df,col):
    ndf = pd.DataFrame(df[col].value_counts()).reset_index().sort_values(by='index')
    ndf = ndf.set_index('index')
    ndf.plot(kind='bar',figsize=(10,4))
    plt.xticks(rotation=90)
    plt.title('number of listings by '+col)
    plt.tight_layout()
    ###
    today = str(dt.date.today())
    filename = today+'_count_listings_by_'+col+'.png'
    path = cwd+'/images'
    os.chdir(path)
    plt.savefig(filename,dpi=300)
    os.chdir(cwd)
    print(cwd)
    return filename
###

def search_craigslist():
    print('start job...')
    # today = str(dt.date.today())
    #now = str(dt.datetime.now()).replace(' ','_').split('.')[0].replace(':','-')
    today = str(dt.date.today())
    csv_filename = today+'_craigslist_app_search_results.csv'
    cl_h = CraigslistHousing(site='sfbay', area='sfc',
                             filters={'min_price': 3000, 'max_price': 7000, 
                                      'search_distance': 4, 'zip_code': 94133,
                                      'min_bedrooms':3})
    ###
    i = 0
    dfs = []
    print('parsing results')
    for result in cl_h.get_results(sort_by='newest', geotagged=True, include_details=True):
        #print(i)
        temp = pd.DataFrame(list(result.items())).T
        cols = list(temp.iloc[0])
        temp.columns = cols
        temp = temp.iloc[-1]
        temp = pd.DataFrame(temp).T
        dfs.append(temp)
        i = i+1
    ###
    print(str(i+1)+' listings collected')
    df = pd.concat(dfs,sort=False)
    df['script_timestamp'] = dt.datetime.now()
    df = clean_craigslist_df(df)
    ###
    bar_chart_filename01 = '/images/'+make_bar_chart(df,'date_available')
    bar_chart_filename02 = '/images/'+make_bar_chart(df,'date_posted')
    new_posts = len(list(df.loc[df['date_posted']==dt.date.today()]['url']))
    new_posts = '\n\n'+str(new_posts)+' new posts today'#:\n\n'+'\n'.join(new_posts)
    ###
    print('saving file...')
    #cwd = os.getcwd()
    path = cwd+'/csvs'
    os.chdir(path)
    df.to_csv(csv_filename,index=False)
    os.chdir(cwd)
    print(cwd)
    print('saved successfully')
    return ['/csvs/'+csv_filename,bar_chart_filename01,bar_chart_filename02], new_posts
###

def combine_craigslist_csvs():
    #cwd = os.getcwd()
    path = cwd+'/csvs'
    os.chdir(path)
    
    extension = 'csv'
    result = glob.glob('*.{}'.format(extension))
    csvs = [i for i in result if 'craigslist' in i]
    dfs = []
    for csv in csvs:
        dfs.append(pd.read_csv(csv))
    ###
    df = pd.concat(dfs,sort=False)
    
    # sort such that the most recent script instance is at the bottom
    df = df.sort_values(by='script_timestamp',ascending=True)
    print('concat csvs \t= ',len(df),' rows')
    
    # keep only the last instance so that the most recent script timestamp is kept
    # datediff between listing and last timestamp can act as a proxy for post longevity
    df = df.drop_duplicates(subset='id',keep='last')
    print('deduped df \t= ',len(df),' rows')
    df['date_script_timestamp'] = pd.to_datetime(df['script_timestamp']).dt.date
    df['currently_listed'] = df['date_script_timestamp'].apply(lambda x: dt.date.today()==x)
    ###
    #now = str(dt.datetime.now()).replace(' ','_').split('.')[0].replace(':','-')
    today = str(dt.date.today())
    csv_filename = today+'_compiled_search_results.csv'
    df = clean_craigslist_df(df)
    ###
    print('saving file...')
    df.to_csv(csv_filename,index=False)
    os.chdir(cwd)
    print(cwd)
    print('saved successfully')
    return 
###

def mail(to, subject, text, attach):
    filenames = attach
    gmail_user = config.myemail
    gmail_pwd = config.password
    ###
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    #get all the attachments
    for file in filenames:
        part = MIMEBase('application', 'octet-stream')
        print(file)
        part.set_payload(open(cwd+file, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % file)
        msg.attach(part)
    ###
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    return mailServer.close()

###
print('\n','-'*6,'run search')
search_result_filenames, new_posts = search_craigslist()
print('\n','-'*6,'run csv aggregator')
# combine_craigslist_csvs()

###
print('\n','-'*6,'send email')
today = str(dt.date.today())
recipients = config.recipients
mail(recipients,
    today+" Craigslist Search Results",
    "Testing automated email for Craigslist search results. For search parameters see: \n https://sfbay.craigslist.org/search/sfc/apa?search_distance=4&postal=94133&min_price=4000&max_price=7000&min_bedrooms=3&availabilityMode=0&sale_date=all+dates"+new_posts+' (not sure if this number is correct)',
    search_result_filenames)
print('program successful!')