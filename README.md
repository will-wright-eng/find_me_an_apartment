# Find Me An Apartment

The first pass at this project was a crude python script that looped over the CraigslistHousing generator, converted results to a pandas dataframe, then send out an email. I manually ran this program on a daily-ish basis from 2020-01-15 till 2020-03-20, prior to my search for a new apartment. 

The second iteration on the project is deploying a reworked version to airflow, which runs on a daily basis.

## Summary
- craigslist search ([github](https://github.com/juliomalegria/python-craigslist))
- data handling
- smtp email ([docs](https://docs.python.org/3/library/smtplib.html))

## Directory

```bash
.
├── README.md
├── images
│   ├── 2020-03-04_count_listings_by_date_available.png
│   ├── 2020-03-04_count_listings_by_date_available_combined_csv.png
│   ├── tableau1.png
│   ├── tableau2.png
│   └── tableau3.png
├── src
│   ├── dag_clist.py
│   ├── main_clist.py
│   ├── main_email.py
│   ├── module_clist
│   │   ├── __init__.py
│   │   └── collect_clist.py
│   ├── module_email
│   │   ├── __init__.py
│   │   ├── email_config.py
│   │   └── send_email.py
│   └── module_utils
│       ├── __init__.py
│       ├── function_logger.py
│       └── s3_funks.py
```

## Results
Analysis included the images sent out in every email along with a Tableau dashboard

### Sample of email images
Count listings by date available
![sample2](https://github.com/william-cass-wright/find_me_an_apartment/blob/master/images/2020-03-04_count_listings_by_date_available.png)
Count listings by date available (combined csv)
![sample1](https://github.com/william-cass-wright/find_me_an_apartment/blob/master/images/2020-03-04_count_listings_by_date_available_combined_csv.png)


### Tableau workbook snapshots
[Tableau Public](https://public.tableau.com/profile/will.wright6939#!/vizhome/2020-07-20_craigslist_listings_analysis_in_sf/MainDashboard)

Dashboard 1
![tableau1](https://github.com/william-cass-wright/find_me_an_apartment/blob/master/images/tableau1.png)
Dashboard 2
![tableau2](https://github.com/william-cass-wright/find_me_an_apartment/blob/master/images/tableau2.png)
Dashboard 3
![tableau3](https://github.com/william-cass-wright/find_me_an_apartment/blob/master/images/tableau3.png)

## Analysis
An interesting observation is that about 80% of posts are automatically re-posted every day for visability -- filtering out these reposts as noise allowed for me to identify the more desirable apartments. 

## To Do
### Need
- ~~add logging in place of print statements~~
- ~~save snapshot tables as ~~parquet~~ csv to S3~~
- add CI (Travis or Jenkins)

### Want
- make sure send_email method can handle w/ and w/o image attachments
- parameterize craigslist search
- develop report into more formal pdf (incorporate Tableau dashboard if possible)

### Nice to have
- Airflow DAG to automate data collection
- simple UI
- managed recipient list (Google Group)
