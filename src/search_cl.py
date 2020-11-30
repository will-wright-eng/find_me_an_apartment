'''
craigslist module

Author: William Wright
'''


def search_craigslist():
    '''docstring for search_craigslist'''
    # print('start job...')
    today = str(dt.date.today())
    csv_filename = today + '_craigslist_app_search_results.csv'
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
    df = clean_craigslist_df(df)

    bar_chart_filename01 = make_bar_chart(df, 'date_available')
    bar_chart_filename02 = make_bar_chart(df, 'date_posted')

    df['date_available'] = pd.to_datetime(df['date_available'])
    df['bedrooms'] = df['bedrooms'].astype(int)
    ndf = df.loc[pd.isnull(df['available']) == False]

    start_date = '2020-03-14'
    stop_date = '2020-04-16'
    ndf0 = ndf.loc[ndf['date_available'] > pd.to_datetime(start_date)]
    ndf0 = ndf0.loc[ndf0['date_available'] < pd.to_datetime(stop_date)]

    ndf0 = ndf0.loc[ndf0['bedrooms'] == 3]

    new_post_links = list(ndf0['url'])
    num_new_posts = len(
        list(df.loc[df['date_posted'] == dt.date.today()]['url']))
    new_post_links = str(len(df)) + ' total posts collected\n' + str(
        num_new_posts
    ) + ' new posts today\n\n' + 'Posts availabile between ' + start_date + ' and ' + stop_date + ' with 3 bedrooms: \n\n' + ' \n\n'.join(
        new_post_links)
    new_posts = new_post_links

    # print('saving file...')
    path = cwd + '/csvs'
    os.chdir(path)
    df.to_csv(csv_filename, index=False)
    os.chdir(cwd)
    # print('saved successfully')
    return [
        '/csvs/' + csv_filename, '/images/' + bar_chart_filename01,
        '/images/' + bar_chart_filename02
    ], new_posts
