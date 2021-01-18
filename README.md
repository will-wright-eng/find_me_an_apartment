# Find Me An Apartment

## Table of Contents

1. [Summary](README.md#summary)
2. [Tree](README.md#tree)
3. [Analysis](README.md#analysis)
4. [To Do](README.md#to-do)

## Summary

The first pass at this project was a crude python script that looped over the CraigslistHousing generator, converted results to a pandas dataframe, then send out an email. I manually ran this program on a daily-ish basis from 2020-01-15 till 2020-03-20, prior to my search for a new apartment. 

The second iteration on the project is deploying a reworked version to airflow running on a Raspberry Pi (in progress).

- craigslist search ([github](https://github.com/juliomalegria/python-craigslist))
- data handling (pandas)
- smtp email ([docs](https://docs.python.org/3/library/smtplib.html))

## Tree
```bash
.
├── README.md
├── agg_analysis
│   ├── agg_csvs_script.py
│   └── myconfigs.py
├── dag_clist.py
├── images
├── src
│   ├── main_clist.log
│   ├── main_clist.py
│   ├── main_email.py
│   ├── module_clist
│   │   ├── __init__.py
│   │   └── collect_clist.py
│   ├── module_email
│   │   ├── README.md
│   │   ├── __init__.py
│   │   └── email_configs.py
│   └── module_utils
│       ├── __init__.py
│       ├── function_logger.py
│       └── s3_funks.py
└── sys_setup
    ├── pi_files_example.sh
    └── scp_zip_example.sh
```

## Analysis
Analysis included the images sent out in every email along with a Tableau dashboard

An interesting observation is that about 80% of posts are automatically re-posted every day for visability -- filtering out these reposts as noise allowed for me to identify the more desirable apartments. 

### Update 2021-01-18
It appears as though listings -- given my search parameters and filtering for the 15 most common neighborhood names -- have dropped in avg/median price by about 50% and increased in quantity by about 10x!

![update](https://github.com/william-cass-wright/find_me_an_apartment/blob/master/images/Screen_Shot_2021-01-15_at_1.13.56_AM.png)

### Tableau workbook snapshots
[Tableau Public 2020](https://public.tableau.com/profile/will.wright6939#!/vizhome/2020-07-20_craigslist_listings_analysis_in_sf/MainDashboard)
[Tableau Public 2021](https://public.tableau.com/profile/will.wright6939#!/vizhome/clistanalysisofSF2021/MainDashboard)

![tableau1](https://github.com/william-cass-wright/find_me_an_apartment/blob/master/images/tableau1.png)

## To Do
### Need
- obligatory blog post of project
- add CI (Travis or Jenkins)
- ~~aggregate analysis/report~~
- conditional dag for daily and aggregate (every 2 weeks) reports
- move py configs to cfg file at the repo level
- ~~Airflow DAG to automate data collection~~
- ~~add logging in place of print statements~~
- ~~save snapshot tables as ~~parquet~~ __csv__ to S3~~

### Want
- parameterize craigslist search
- develop report into more formal pdf (incorporate Tableau dashboard if possible)
- update Tableau public dashboard (last done 2021-01-18)
- convert dashboard over to Superset
- __deployt airflow dag to raspberry pi__
- ~~make sure send_email method can handle w/ and w/o image attachments~~

### Nice to have
- simple UI for new searches and implementation
- managed recipient list via Google Group
