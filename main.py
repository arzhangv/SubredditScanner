# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import boto3
import requests
import json
import time
import os.path
from os import path
import os, glob, json, csv
import pandas as pd
import sys
from boto.s3.key import Key


from datetime import datetime, timedelta

class Reddit_Data:
    def move_data_to_S3(self):
       s3 = boto3.client('s3',
            aws_access_key_id='',
            aws_secret_access_key='',

        )

       bucket_name = 'arzhangvredditdata'
       path = "Comments_CSV"

     #  s3.put_object(Bucket=, Key=(directory_name + '/'))
       #for filename in os.listdir(path):

       #     f = os.path.join(path, filename)

       s3.put_object(Bucket=bucket_name, Key='test-folder/')
       
       #file_path = "C:\\Users\\Arzhang\\PycharmProjects\\getRedditData\\Comments_CSV"
       #with open(file_path + "\\blackhat_comments.csv", 'rb') as data:
           #s3.upload_fileobj(data, 'arzhangvredditdata', 'blackhat_comments.csv')

    def datespan(self,startDate, endDate, delta=timedelta(days=1)):
        currentDate = startDate
        while currentDate < endDate:
            yield currentDate
            currentDate += delta

    #epoch time value to add to url of request
    def get_epoch_time(self, rawtime):
        epoch_time = rawtime.timestamp()
        return int(epoch_time)

    def writeToFileSubmission(self ,subreddit_name, date, data):
        date_adjusted = date.replace(" ", "")
        date_adjusted = date_adjusted.replace("-", "_")
        date_adjusted = date_adjusted.replace(":", "_")

        fileName = subreddit_name + "Submission" + date_adjusted + ".json"
        filePath = "C:\\Users\\Arzhang\\PycharmProjects\\getRedditData\\malwareSubmission"
        file = filePath + "\\" + fileName

        with open(file, "w") as outfile:
            json.dump(data, outfile)
    def writeToFile(self, subreddit_name, date, data):
        date_adjusted = date.replace(" ", "")
        date_adjusted = date_adjusted.replace("-", "_")
        date_adjusted = date_adjusted.replace(":", "_")

        fileName = subreddit_name + date_adjusted + ".json"
        filePath = "C:\\Users\\Arzhang\\PycharmProjects\\getRedditData\\" + subreddit_name + "Comments"
        file = filePath +  "\\"+ fileName

        with open(file, "w") as outfile:
            json.dump(data, outfile)


    def writeJSONSubmissionToCSV(self):
        subreddits = ["Hacking_Tutorials_submissions"]
        #subreddits = [ "privacy_submissions","blackhat_submissions", "cybersecurity_submissions", "hacking_submissions","Hacking_Tutorials_submissions", "computerforensics_submissions"]
        for i in subreddits:
            filepath = "C:\\Users\\Arzhang\\PycharmProjects\\getRedditData\\subredditDataFromRedditor\\" + i + ".json"
            root_url = "https://www.reddit.com/"
            data_dict = {
                "Post ID": [],
                "Comment ID": [],
                "Username": [],
                "Body": [],
                "Subreddit": [],
                "Date": [],
                "Score": [],
                "Embedded URL": [],
                "URL": []
            }
            with open(filepath, 'r', encoding='utf-8') as f:
                try:

                    for line in f:
                            data = json.loads(line)
                            data_dict['Post ID'].append(data['id'])
                            data_dict['Comment ID'].append(data['id'])
                            data_dict['Username'].append(data['author'])
                            data_dict['Body'].append(data['selftext'])
                            created_utc = datetime.fromtimestamp( int(data['created_utc']))
                            data_dict['Date'].append(created_utc)
                            data_dict['Subreddit'].append(data['subreddit'])
                            data_dict['Embedded URL'].append(data['url'])
                            data_dict['URL'].append(root_url + data['permalink']+".com")
                            data_dict['Score'].append(data['score'])
                except UnicodeDecodeError:
                    print("UnicodeDecodeError")

            df = pd.DataFrame(data_dict)
            df.to_csv("C:\\Users\\Arzhang\\PycharmProjects\\getRedditData\\Submissions_CSV\\"+ i +".csv")


    def writeJSONCommentToCSV(self):
        subreddits = ["Hacking_Tutorials_comments"]
        #subreddits = ["privacy_comments", "blackhat_comments", "cybersecurity_comments", "hacking_comments", "Hacking_Tutorials_comments", "computerforensics_comments"]
        for i in subreddits:
            filepath = "C:\\Users\\Arzhang\\PycharmProjects\\getRedditData\\subredditDataFromRedditor\\" + i + ".json"
            #filepath = "/Users/arzhangvaladkhani/PycharmProjects/redditRequestParser/Comments/" + i + ".json"
            root_url = "https://www.reddit.com/"
            data_dict = {
                "Post ID": [],
                "Comment ID": [],
                "Username": [],
                "Body": [],
                "Subreddit": [],
                "Date": [],
                "Score": [],
                "Embedded URL": [],
                "URL": []

            }
            with open(filepath, 'r', encoding='utf-8') as f:
                try:

                    for line in f:
                            data = json.loads(line)
                            post_id = data['link_id'].replace("t3_", "")
                            data_dict['Post ID'].append(post_id)
                            data_dict['Comment ID'].append(data['id'])
                            data_dict['Username'].append(data['author'])
                            data_dict['Body'].append(data['body'].replace("\r", "\\r"))

                            #created_utc = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(data['Date'])))
                            #created_utc = datetime.strptime(created_utc, "%Y-%m-%d %H:%M:%S")
                            time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(data['created_utc'])))
                            created_utc = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(data['created_utc'])))
                            data_dict['Date'].append(created_utc)
                            data_dict['Subreddit'].append(data['subreddit'])
                            data_dict['Score'].append(data['score'])
                            data_dict['Embedded URL'].append("NA")
                            data_dict['URL'].append("NA")
                except UnicodeDecodeError:
                    print("UnicodeDecodeError")

            df = pd.DataFrame(data_dict)
            df.to_csv("C:\\Users\\Arzhang\\PycharmProjects\\getRedditData\\Comments_CSV\\" + i + ".csv")
            #df.to_csv("/Users/arzhangvaladkhani/PycharmProjects/redditRequestParser/comments_csv/privacy_comments.csv")


    def get_subreddit_data(self, subreddit, before, after):
        epoch_before = str(self.get_epoch_time(before))
        epoch_after = str(self.get_epoch_time(after))
        try:
            #https://api.pushshift.io/reddit/comment/search?html_decode=true&after=1314342000&before=1314514800&subreddit=blackhat&size=10
            #response = requests.get("https://api.pushshift.io/reddit/comment/search?html_decode=true&after=1314342000&before=1314514800&subreddit=blackhat&size=100")
            response = requests.get("https://api.pushshift.io/reddit/search/comment/?after="+ epoch_before +"&before=" + epoch_after +"&subreddit="+ subreddit + "&size=1000")
            time.sleep(1.5)
            #submission_response = requests.get("https://api.pushshift.io/reddit/search/submission/?after="+ epoch_before +"&before=" + epoch_after +"&subreddit=malware" + "&size=1000")

        except "Too Many Requests" in response.text :
            print("waiting to get all requests")
            time.sleep(10)
            response = requests.get("https://api.pushshift.io/reddit/search/comment/?after="+ epoch_before +"&before=" + epoch_after +"&subreddit=" + subreddit+ "&size=1000")

        try:
            print(before)
            print(response.text)
            response_dict = json.loads(response.text)
            #submission_response_dict = json.loads(submission_response.text)
            self.writeToFile( subreddit, str(before), response_dict)

            #self.writeToFileSubmission("malware",str(before), submission_response_dict)

        except json.decoder.JSONDecodeError:
            response_dict = None
            print(response_dict)
    def process_JSON_to_CSV(self, subreddit):
        directory = "C:\\Users\\Arzhang\\PycharmProjects\\getRedditData\\" + subreddit +"Comments"
        list_of_data = []
        dict1 = {}
        data_dict = {
            "Post ID": [],
            "Username": [],
            "Comment Body": [],
            "CommentID": [],
            "Date": [],
            "Score": []

        }

        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            # new_name = str(f) + ".json"
            # os.rename(f, new_name)
            try:
                with open(f, 'r') as file:
                    temp_data = json.load(file)
                    temp_data2 = temp_data['data']
                    for data in temp_data2:
                        data_dict['Post ID'].append(data['link_id'])
                        data_dict['Username'].append(data['author'])
                        data_dict['Comment Body'].append(data['body'])
                        data_dict['Date'].append(data['utc_datetime_str'])
                        data_dict['CommentID'].append(data['id'])
                        data_dict['Score'].append(data['score'])
            except OSError:
                continue




        df = pd.DataFrame(data_dict)
        df.to_csv("C:\\Users\\Arzhang\\PycharmProjects\\getRedditData\\"+subreddit+"Comments.csv")

    def master_loop(self):
        i = 0#"hacking","hacking_tutorials", "howtohack", "cybersecurity"
        list_of_subreddits = [ "blackhat"]
        for subreddit in list_of_subreddits:
            for timestamp in self.datespan(datetime(2011, 8, 26, 0,1), datetime(2011, 9, 2, 0, 1),delta=timedelta(days=1)):
                if i == 0:
                    before = timestamp
                elif i == 1:
                    after  = timestamp
                else:
                    self.get_subreddit_data(subreddit,before, after)
                    prev = after
                    next = timestamp
                    before = after
                    after = next
                i+= 1
           #self.process_JSON_to_CSV(subreddit)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    reddit = Reddit_Data()
    reddit.writeJSONSubmissionToCSV()
    reddit.writeJSONCommentToCSV()
    #reddit.move_data_to_S3()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/# This is a sample Python script.

