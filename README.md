# Subreddit Scanner 
 
- This is an all in one tool for users to scrape subreddit data at scale and run indepth analysis on user activity read in [my research paper](https://github.com/arzhangv/SubredditScanner/blob/main/SubredditScanner_Report.pdf).

- Gain further understing at scale using state of the art clustering algorithms and LDA topic modeling. 

- The pipeline for data collection, storage, analysis, and machine learning is explained in the diagram below.
&nbsp;
&nbsp;


***
<p align="center">
  <img src="https://github.com/arzhangv/SubredditScanner/blob/main/DiagramV3.png" />
</p>

***

### Data Scraper
- Making requests on two PushShiftIO endpoints on submissions and comments respectively 
- The Query is structured as so scrape data with three parameters and the code is listed below: 
  1. Subreddit 
  2. Before (Epoch value or Integer + "s,m,h,d")
  3. After (Epoch value or Integer + "s,m,h,d")
- For more details on PushShiftIO documentation visit https://github.com/pushshift/api
```python
response = requests.get("https://api.pushshift.io/reddit/search/comment/?after="+ epoch_before +"&before=" + epoch_after +"&subreddit="+subreddit + "&size=1000")

```
```python
response = requests.get("https://api.pushshift.io/reddit/search/submission/?after="+ epoch_before +"&before=" + epoch_after +"&subreddit="+subreddit + "&size=1000")

```
- The maximum number of posts that can be returned in one request is 1000 so its important to note that highly active subreddits which can have over 1000 comments or posts in a day. Therefore must have the duration of that is parameters before and after be lessend to extrapulate all posts in a timeframe. 
***
### Storage
- Configure storage to Amazon S3 buckets and locally as well. 
&nbsp;
&nbsp;
- Input AWS credentials to gain access to your S3 bucket located in line 33 in main.py

```python
 s3 = boto3.client('s3',
            aws_access_key_id='your-access-key',
            aws_secret_access_key='your-secret-access-key',
        )
```

- Edit lines to select which file, S3 bucket, and the key you would like to utilize
&nbsp;
&nbsp;
```python
       s3.upload_file(
       Filename="data/send_a_certain.csv",
       Bucket="sample-bucket-1801",
       Key="new_file.csv")
     
```
&nbsp;
&nbsp;
*** 
### Data Model 

- PushshiftAPI comment and submission responses are quite extensive, and need to be processed and parsed accordingly 
- The data is modeled to the values displayed in the table below. 

Post ID | Comment ID | Username | Body | Date | URL | Score | Subreddit Name |
--- | --- | --- | --- | --- | ---  | --- | --- | 


