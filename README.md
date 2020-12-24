# Find Me An Apartment

## Table of Contents

1. [Summary](README.md#summary)
2. [Tree](README.md#tree)
3. [Analysis](README.md#analysis)
4. [To Do](README.md#to-do)

## Summary

The first pass at this project was a crude python script that looped over the CraigslistHousing generator, converted results to a pandas dataframe, then send out an email. I manually ran this program on a daily-ish basis from 2020-01-15 till 2020-03-20, prior to my search for a new apartment. 

The second iteration on the project is deploying a reworked version to airflow, which runs on a daily basis.

- craigslist search ([github](https://github.com/juliomalegria/python-craigslist))
- data handling (pandas)
- smtp email ([docs](https://docs.python.org/3/library/smtplib.html))

## Tree

```bash
.
├── README.md
├── dag_clist.py
├── images
│   ├── 2020-03-04_count_listings_by_date_available.png
│   ├── 2020-03-04_count_listings_by_date_available_combined_csv.png
│   ├── tableau1.png
│   ├── tableau2.png
│   └── tableau3.png
├── scp_zip.sh
├── src
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
│       ├── __init__.py
│       ├── function_logger.py
│       └── s3_funks.py
└── src.zip
```

## Analysis
Analysis included the images sent out in every email along with a Tableau dashboard

An interesting observation is that about 80% of posts are automatically re-posted every day for visability -- filtering out these reposts as noise allowed for me to identify the more desirable apartments. 

### Tableau workbook snapshots
[Tableau Public](https://public.tableau.com/profile/will.wright6939#!/vizhome/2020-07-20_craigslist_listings_analysis_in_sf/MainDashboard)

![tableau1](https://github.com/william-cass-wright/find_me_an_apartment/blob/master/images/tableau1.png)

## To Do
### Need
- obligatory blog post of project
- add CI (Travis or Jenkins)
- aggregate analysis/report
- conditional dag for daily and aggregate (every 2 weeks) reports
- ~~Airflow DAG to automate data collection~~
- ~~add logging in place of print statements~~
- ~~save snapshot tables as ~~parquet~~ __csv__ to S3~~

### Want
- parameterize craigslist search
- develop report into more formal pdf (incorporate Tableau dashboard if possible)
- update Tableau public dashboard
- convert dashboard over to Superset
- ~~make sure send_email method can handle w/ and w/o image attachments~~

### Nice to have
- simple UI for new searches and implementation
- managed recipient list (Google Group)
