'''
generate report on historical data

Author: William Wright
'''


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