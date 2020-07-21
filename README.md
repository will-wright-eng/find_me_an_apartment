# Find Me An Apartment

This project was devised to better understand the rental market in SF. I manually ran this program on a daily (ish) basis from 2020-01-15 till 2020-03-20, prior to my search for a new apartment. 

## craigslist_extract_and_email
This module includes:
- craigslist search
- data handling
- smtp email

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

## Enhancments
- Airflow DAG to automate data collection
- simple UI
- parameterize craigslist search