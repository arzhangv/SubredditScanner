#####################      Author: RISUL ISLAM                 ###############################
#####################      University of California, Riverside ###############################
#####################      Paper: TenFor                       ###############################


# Disclaimer: This is the demo code for TenFor. We will keep updating continupously.
# PLease let us know if you need more details or any corrention.
# Reach me directly at: risla002@ucr.edu
import json

import sparse
import pandas as pd
import tensorly as tl
import numpy as np
import matplotlib.pyplot as plt


import matplotlib.patches as mpatches
import random

print("Half imported")

from datetime import datetime
from datetime import timedelta
import random
#from unidecode import unidecode
from tensorly.contrib.sparse.decomposition import non_negative_parafac
import tensorly.contrib.sparse as tl
import pickle
#from gensim.summarization.summarizer import summarize
#from gensim.summarization import keywords

print("Full imported")

# parameters
rank = 11  # idea number of clusters to be decomposed into. In future, we will use autoTen output here.
post_limit = 5  # for primary filtering for removing threads with lower number of replies.
topk = 5  # top k user, thread, time, titles

# input your own csv filename and columnnames here.
df = pd.read_csv("Sub_and_Com_CSV/blackhat.csv")  # input your own csv file here. here there should be thread ID, title, thread initializer usernames, initilization date of the thread
print("thread File read")

print(df.columns.tolist())

tusernames = df['Username']
tdates = df['day-month-yr']
ttids = df['Post ID']
#ttitles = df['title']

print("Total lines: ", len(ttids))
usernames = df['Username']
dates = df['day-month-yr']
thread_ids = df['Post ID']
# input your own csv filename and columnnames here. here there should be thread ID, post ID, post usernames, post date.
'''#dfposts = pd.read_csv("reddit_post_oct.csv")
print("post File read")

print(dfposts.columns.tolist())

pusernames = dfposts['author_name']
pdates = dfposts['date']
ppids = dfposts['id']
ptids = dfposts['thread_id']

print("Total posts: ", len(ppids))'''#dfposts = pd.read_csv("reddit_post_oct.csv")



# filtering the threads with lowest replies
'''def filtered_cut_thread(ptids, pusernames):
    print("thread filtering on progress... ")
    map_thread_post = {}

    cut_threads = []
    for i in range(0, len(ptids)):

        if type(pusernames[i]) == str:
            if ptids[i] not in map_thread_post:
                map_thread_post[ptids[i]] = 1
            else:
                map_thread_post[ptids[i]] += 1

    for tid in map_thread_post.keys():
        if map_thread_post[tid] > post_limit:
            cut_threads.append(tid)
    print("Cut threads: ", len(cut_threads))

    return cut_threads, map_thread_post


cut_threads, map_thread_post = filtered_cut_thread(ptids, pusernames)'''


# map entity (username, thread, time) with a unique id
def create_map_id_entity(entity):
    j = 0
    map_entity_id = {}
    map_id_entity = {}
    for i in range(len(entity)):
        e = entity[i]
        if e not in map_entity_id.keys(): #and ttids[i] in cut_threads:
            map_entity_id[e] = j
            map_id_entity[j] = e
            j += 1

    return map_entity_id, map_id_entity


map_username_id, map_id_username = create_map_id_entity(usernames)
map_thread_id, map_id_thread = create_map_id_entity(thread_ids)
map_date_id, map_id_date = create_map_id_entity(dates)


'''def create_map_id_date(tdates):
    j = 0
    map_date_id = {}
    map_id_date = {}
    for i in range(len(tdates)):
        e = tdates[i]

        Tindex = e.find("T")
        date = e[0:Tindex]

        if date not in map_date_id.keys():
            map_date_id[date] = j
            map_id_date[j] = date
            j += 1

    return map_date_id, map_id_date


map_date_id, map_id_date = create_map_id_date(tdates)'''

user_dimension = len(map_username_id.keys())
thread_dimension = len(map_thread_id.keys())
time_dimension = len(map_date_id.keys())

print("Distinct users: ", user_dimension)
print("Distinct threads: ", thread_dimension)
print("Distinct times: ", time_dimension)

# Construct hte Tensor here
def construct_tensor_matrix(ptids, pusernames, pdates, map_indexed_user, map_indexed_thread, map_indexed_time):
    x = len(map_indexed_user)
    y = len(map_indexed_thread)
    z = len(map_indexed_time)

    #mat = np.zeros((x, y, z))
    coords = []
    coords.append([])
    coords.append([])
    coords.append([])
    vals = []



    print("Creating the tensor, may take time")
    for i in range(0, len(ptids)):

        if type(pusernames[i]) == str:
            u = pusernames[i].replace('"', '')
            th = ptids[i]
            t = pdates[i]


            if u in map_indexed_user and th in map_indexed_thread and t in map_indexed_time:
                uind = np.int64(map_indexed_user[u])
                thind = np.int64(map_indexed_thread[th])
                tind = np.int64(map_indexed_time[t])

                #mat[uind][thind][tind] += 1
                xcoords = coords[0]
                ycoords = coords[1]
                zcoords = coords[2]

                index = -1
                for k in range(len(xcoords)):
                    if(xcoords[k] == uind and ycoords[k] == thind and zcoords[k] == tind  ):
                        index = k
                        break
                if(index != -1):
                    vals[index] += 1
                else:
                    xcoords.append(uind)
                    ycoords.append(thind)
                    zcoords.append(tind)
                    vals.append(1)

        if (i + 1) % 10000 == 0:
            print("post already read ", i)
    mat = sparse.COO(coords, vals, shape=(x,y,z))
    print(type(mat))
    print(mat)
    return mat


mat = construct_tensor_matrix(thread_ids, usernames, dates, map_username_id, map_thread_id, map_date_id)

print("Dimensions: ", mat.shape)


# drawing the scree plots and other necessary graphs. Create a folder named "figuresAnomalous" for this part
def draw_barchart(x, y, xlabel, ylabel):
    """
    plt.bar(x,y,align='center') # A bar chart
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    #for i in range(len(y)):
        #plt.hlines(y[i],0,x[i]) # Here you are drawing the horizontal lines
    """
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    ax.bar(np.arange(len(x)), y, log=1)
    ax.set_xticks(np.arange(len(x)))
    ax.set_xticklabels(x, rotation=45, zorder=100)
    plt.ylabel(ylabel)

    directory = "figuresAnomalous/Bar chart for " + ylabel + " VS " + xlabel
    plt.savefig(directory)
    plt.close()


# filtering threadhold calculation to filter out the weak entities from each cluster.
# In future we will add regularization with Tensor decomsition itself
def findthreshold(a):
    howmanysdv = 0
    avg = sum(a) / len(a)
    sd = np.std(a)
    return (avg + (sd * howmanysdv))


# filter out the weak entities from each cluster
def find_anomalous_component(userdataset, threaddataset, xlabel, ylabel, thresholduser, thresholdthread, part):
    map_user_thread_count_component = {}
    map_component_dimension = {}
    map_component_dimension_value = {}
    for i in range(0, len(userdataset)):
        valid_user_count = 0
        thrs = findthreshold(userdataset[i])
        unum = 0
        ulist = []
        vallist = []
        for user in userdataset[i]:
            if user >= thrs:
                valid_user_count += 1
                if part == 1:
                    ulist.append(map_id_username[unum])
                    vallist.append(user)
                elif part == 2:
                    ulist.append(map_id_thread[unum])
                    vallist.append(user)
                else:
                    ulist.append(map_id_date[unum])
                    vallist.append(user)
            unum += 1
        print("Component: ", i)
        print(ulist)
        map_component_dimension[i] = ulist
        map_component_dimension_value[i] = vallist

        valid_thread_count = 0;
        thrs = findthreshold(threaddataset[i])
        for t in threaddataset[i]:
            if t >= thrs:
                valid_thread_count += 1

        map_user_thread_count_component[i] = [valid_user_count, valid_thread_count]
    x = []
    y = []
    C = []
    for key in sorted(map_user_thread_count_component):
        x.append(map_user_thread_count_component[key][0])
        y.append(map_user_thread_count_component[key][1])

        C.append(key)
        print("Valid ", xlabel, " count: ", key, " Component: ", map_user_thread_count_component[key][1])
        print("Valid ", ylabel, " count: ", map_user_thread_count_component[key][0], " Component: ",
              map_user_thread_count_component[key][1])

    plt.plot(x, y, 'r.')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    directory = "figuresAnomalous/Scree plot for " + ylabel + " VS " + xlabel
    plt.savefig(directory)
    plt.close()

    draw_barchart(C, x, "Component Number", xlabel)
    return map_component_dimension, map_component_dimension_value


# Main decompsition is here. Currently regulation is missing here.
# Thats why we used another average and std based filtering to cut out the weak entities from each component.
# Visualize each comnent as well.
# Create a folder named "figures"  for this part.

def analyze_with_tensor_decomposition(mat, x, y, z):
    print("Tensor Decomposition starts...")
    tensor = tl.tensor(mat, dtype=np.float64)
    # tensor = tl.tensor(np.arange(24).reshape((3, 4, 2)))
    print("The given tensor:")

    start_analysis_fignmbr = 0

    weights, factors = non_negative_parafac(tensor, rank=rank, init='random', verbose=5)

    print("Factors: ")
    print(factors)

    print("Slice: ")
    print(factors[0])
    print(list(factors[0][:, 0]))
    user = [i for i in range(0, x)]
    print(user)
    thread = [i for i in range(0, y)]
    time = [i for i in range(0, z)]

    userdataset = []
    threaddataset = []
    timedataset = []

    print("Tensor figures drawing..")
    plt.figure(1)
    for i in range(start_analysis_fignmbr, rank * 3):
        fignmbr = (i % 3) + 1
        col = int(i / 3)
        row = int(i % 3)

        print("row: ", row, " col: ", col, " fignmbr: ", fignmbr)
        y = list(factors[row][:, col])
        # print(y)

        ax = plt.subplot(1, 3, fignmbr)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        if i % 3 == 0:
            plt.plot(user, y, 'r.')
            plt.xlabel("User")
            userdataset.append(y)

        if i % 3 == 1:
            plt.plot(thread, y, 'c.')
            plt.xlabel("Thread")
            threaddataset.append(y)

        if i % 3 == 2:
            plt.plot(time, y, 'g.')
            plt.xlabel("Monthly TIme Bin")
            timedataset.append(y)

        if fignmbr % 3 == 0:
            directory = 'figures/component ' + str(int((i + 1) / 3))
            plt.savefig(directory)

            plt.close()

    u_t = 0.1;  # these values are invalid because threshold are calculated inside the callee function
    th_t = 0.05
    t_t = 0.005

    print("Finding and drawing scree plots in figure anamalous...")
    map_component_userlist, map_component_user_value = find_anomalous_component(userdataset, threaddataset,
                                                                                "Number of User", "Number of Thread",
                                                                                u_t, th_t, 1)
    map_component_timelist, map_component_time_value = find_anomalous_component(timedataset, userdataset,
                                                                                "Number of Time Bin", "Number of User",
                                                                                t_t, u_t, 3)
    map_component_threadlist, map_component_thread_value = find_anomalous_component(threaddataset, timedataset,
                                                                                    "Number of Thread",
                                                                                    "Number of Time Bin", th_t, t_t, 2)
    print("checking")
    print(map_component_userlist.keys())
    print(map_component_userlist[0])
    print(map_component_user_value[0])
    return map_component_userlist, map_component_user_value, map_component_timelist, map_component_time_value, map_component_threadlist, map_component_thread_value


map_component_userlist, map_component_user_value, map_component_timelist, map_component_time_value, map_component_threadlist, map_component_thread_value = analyze_with_tensor_decomposition(mat, user_dimension, thread_dimension, time_dimension)


# Save the cluster entities in a pickle file for sharing purpose.

def pickledump(map_component_entity, filename):
    fname = filename + ".pickle"
    pickle_out = open(fname, "wb")
    pickle.dump(map_component_entity, pickle_out)
    pickle_out.close()

def jsondump(map_component_entity, subreddit):
    file = "tenForClusterOutput\\"+subreddit+"\\" ".json"
    with open(file, "w") as outfile:
        json.dump(map_component_entity, outfile)
pickledump(map_component_userlist, "map_component_userlist")
pickledump(map_component_user_value, "map_component_user_value")
pickledump(map_component_timelist, "map_component_timelist")
pickledump(map_component_time_value, "map_component_time_value")
pickledump(map_component_threadlist, "map_component_threadlist")
pickledump(map_component_thread_value, "map_component_thread_value")

jsondump(map_component_userlist, "map_component_userlist")
jsondump(map_component_user_value, "map_component_user_value")
jsondump(map_component_timelist, "map_component_timelist")
jsondump(map_component_time_value, "map_component_time_value")
jsondump(map_component_threadlist, "map_component_threadlist")
jsondump(map_component_thread_value, "map_component_thread_value")
# Return topk entities per cluster
'''{
    component:
        "dates":[]
        "users":[]
        "threads":[]
}'''
def returntopk(map_component_value, map_component_entitylist, outfile):

    for component in map_component_value.keys():
        print("Component ", component)
        outfile.write("Component "+  str(component)+ '\n')
        values = map_component_value[component]
        map_userid_value = {}
        for i in range(len(values)):
            map_userid_value[i] = values[i]

        k = 0;
        for key in sorted(map_userid_value.items(), key=lambda x: x[1], reverse=True):
            k += 1
            print(map_component_entitylist[component][key], map_userid_value[key])
            outfile.write(str(map_component_entitylist[component][key]) + str(map_userid_value[key])+ '\n')

            if (k == topk):
                break

outfile = open('clusters.txt', 'w')
print("Top k users: ")
outfile.write("Top k users: \n")
returntopk(map_component_user_value, map_component_userlist, outfile)

print("Top k threads: ")
outfile.write("Top k threads: \n")

returntopk(map_component_thread_value, map_component_threadlist, outfile)

print("Top k dates: ")
outfile.write("Top k dates: \n")

returntopk(map_component_time_value, map_component_timelist, outfile)

'''
def constructmap_thread_title():
    map_thread_title = {}
    for i in range(len(ttids)):
        map_thread_title[ttids[i]] = ttitles[i]

    return map_thread_title


map_thread_title = constructmap_thread_title()


# Summarize Each cluster top k sentences. [Storyline view]
def returntopktitle(map_component_threadlist):
    for component in map_component_threadlist.keys():
        print("Component ", component)
        threads = map_component_value[component]
        alltitles = ""
        for th in threads:
            alltitles += map_thread_title[th].replace(".", " ") + "."
        summarytext = summarize(alltitles, word_count=1000)

        sentence_count = 0
        resulttopk = ""
        for i in range(len(summarytext)):
            resulttopk += summarytext[i]
            if summarytext[i] == '.':
                sentence_count += 1

                if sentence_count == topk:
                    print(resulttopk)


returntopktitle(map_component_threadlist)'''