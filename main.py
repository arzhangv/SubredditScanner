# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import json
import time
import os.path
from os import path
import os, glob, json, csv
import pandas as pd


from datetime import datetime, timedelta

class Reddit_Data:
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
        filePath = "C:\\Users\\Arzhang\\PycharmProjects\\getRedditData\\malware"
        file = filePath +  "\\"+ fileName

        with open(file, "w") as outfile:
            json.dump(data, outfile)





    def get_subreddit_data(self, before, after):
        epoch_before = str(self.get_epoch_time(before))
        epoch_after = str(self.get_epoch_time(after))
        try:
            response = requests.get("https://api.pushshift.io/reddit/search/comment/?after="+ epoch_before +"&before=" + epoch_after +"&subreddit=malware" )
            time.sleep(2)
            #submission_response = requests.get("https://api.pushshift.io/reddit/search/submission/?after="+ epoch_before +"&before=" + epoch_after +"&subreddit=malware")

        except "Too Many Requests" in response.text :
            print("waiting to get all requests")
            time.sleep(10)
            response = requests.get("https://api.pushshift.io/reddit/search/comment/?after="+ epoch_before +"&before=" + epoch_after +"&subreddit=malware" )





        try:
            print(before)
            print(response.text)
            response_dict = json.loads(response.text)
            #submission_response_dict = json.loads(submission_response.text)
            self.writeToFile( "malware", str(before), response_dict)

            #self.writeToFileSubmission("malware",str(before), submission_response_dict)

        except json.decoder.JSONDecodeError:
            response_dict = None
            print(response_dict)
    def process_JSON_to_CSV(self):
        directory = "C:\\Users\\Arzhang\\PycharmProjects\\getRedditData\\malware"
        list_of_data = []
        dict1 = {}
        data_dict = {

            "Post ID": [],
            "Username": [],
            "Comment Body": [],
            "CommentID":[],
            "Date": [],
            "Score": []
        }
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            # new_name = str(f) + ".json"
            # os.rename(f, new_name)
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



        df = pd.DataFrame(data_dict)
        df.to_csv("C:\\Users\\Arzhang\\PycharmProjects\\getRedditData\\malwareComments.csv")

    def master_loop(self):
        i = 0
        for timestamp in self.datespan(datetime(2017, 8, 16, 0,1), datetime(2023, 1, 3, 0, 1),delta=timedelta(days=1)):
            if i == 0:
                before = timestamp
            elif i == 1:
                after  = timestamp
            else:
                self.get_subreddit_data(before, after)
                prev = after
                next = timestamp
                before = after
                after = next
            i+= 1

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    reddit = Reddit_Data()
    reddit.process_JSON_to_CSV()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/