# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import json
import os.path
from os import path


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
        response = requests.get("https://api.pushshift.io/reddit/search/comment/?after="+ epoch_before +"&before=" + epoch_after +"&subreddit=malware" )

        try:
            print(before)
            print(response.text)
            response_dict = json.loads(response.text)
            self.writeToFile( "malware", str(before), response_dict)

        except json.decoder.JSONDecodeError:
            response_dict = None
            print(response_dict)

    def master_loop(self):
        i = 0
        for timestamp in self.datespan(datetime(2021, 1, 1, 0,1), datetime(2023, 1, 3, 0, 1),delta=timedelta(days=1)):
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
    reddit.master_loop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/