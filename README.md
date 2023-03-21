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
- Making requests on PushShiftIO endpoints on submissions and comments
- The Query is structured as so scrape data with three parameters: 
  1. Subreddit 
  2. Before (Epoch value or Integer + "s,m,h,d")
  3. After (Epoch value or Integer + "s,m,h,d")
- For more details on PushShiftIO documentation visit https://github.com/pushshift/api
```python
            response = requests.get("https://api.pushshift.io/reddit/search/comment/?after="+ epoch_before +"&before=" + epoch_after +"&subreddit="+subreddit + "&size=1000")

```
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
