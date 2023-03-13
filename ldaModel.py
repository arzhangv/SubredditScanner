# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os, glob, json, csv
import numpy as np
import gensim
import pandas as pd
import tqdm
from pprint import pprint
# Tokenize the documents.
import nltk
import tqdm
from gensim import corpora
from nltk.tokenize import RegexpTokenizer
import matplotlib.pyplot as plt
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.models import Phrases, LdaMulticore, CoherenceModel
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from nltk.corpus import stopwords


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
def compute_coherence_values(corpus, dictionary, k, a, b):
    pass


if __name__ == '__main__':

    df = pd.read_csv('C:\\Users\\Arzhang\\PycharmProjects\\getRedditData\\Sub_and_Com_CSV\\Hacking_Tutorials.csv')
    #Setting up dictionaries to store the users, threadIDs, and dates
    user_cluster = {}
    threadID_cluster = {}
    date_cluster = {}
    rank ="4"
    subreddit = "How_To_Hack"
    deletedUsers = "NoDeletedUsers"
    clusterName ="C:\\Users\\Arzhang\\PycharmProjects\\getRedditData\\tenForClusterOutputs\\" + subreddit + deletedUsers + "\\"
    for rank in  range(21, 35 ):
        with open(clusterName + str(rank)+"_map_component_userlist.json") as user_json:
            user_cluster = json.load(user_json)
        with open(clusterName +  str(rank)+"_map_component_threadlist.json") as threadID:
            threadID_cluster = json.load(threadID)
        with open(clusterName +  str(rank)+"_map_component_timelist.json") as date:
            date_cluster = json.load(date)
        print(user_cluster)
        print(threadID_cluster)
        print(date_cluster)
        tokenizer = RegexpTokenizer(r'\w+')

        users_dict = { }
        threads_dict = { }
        dates_dict = { }
        new_df = pd.DataFrame()

        for users, threads, dates in zip(user_cluster.values(), threadID_cluster.values(), date_cluster.values()):
            for i in range(len(users)):
                users_dict[users[i]] = i
            for i in range(len(threads)):
                threads_dict[threads[i]] = i
            for i in range(len(dates)):
                dates_dict[dates[i]] = i

        body = []
        for index, row in df.iterrows():

            if (row['Username'] in users_dict.keys()) & (row['Post ID'] in threads_dict.keys()) & (row['day-month-yr'] in dates_dict.keys()):
                body.append(row['Body'])
        print(new_df)
        docs = []
        for i in body:

            if str(i)== 'nan':

                continue
            if len(str(i)) >= 1:
                docs.append(str(i))



        for idx in range(len(docs)):
            docs[idx] = docs[idx].lower()  # Convert to lowercase.
            docs[idx] = tokenizer.tokenize(docs[idx])  # Split into words.
        # Remove numbers, but not words that contain numbers.
        all_stopwords = stopwords.words('english')

        docs = [[token for token in doc if not token.isnumeric() and token not in all_stopwords] for doc in docs]

        # Remove words that are only one character.
        docs = [[token for token in doc if len(token) > 1] for doc in docs]

        #Remove the pronouns using pos tagging

        # Lemmatize the documents.
        lemmatizer = WordNetLemmatizer()
        docs = [[lemmatizer.lemmatize(token) for token in doc] for doc in docs]
        data_lemetized = docs
        # Add bigrams and trigrams to docs (only ones that appear 20 times or more).
        bigram = Phrases(docs, min_count=20)
        for idx in range(len(docs)):
            for token in bigram[docs[idx]]:
                if '_' in token:
                    # Token is a bigram, add to document.
                    docs[idx].append(token)
        # Create a dictionary representation of the documents.
        dictionary = Dictionary(docs)



        # Filter out words that occur less than 20 documents, or more than 50% of the documents.
        dictionary.filter_extremes(no_below=20, no_above=0.5)
        # Bag-of-words representation of the documents.
        corpus = [dictionary.doc2bow(doc) for doc in docs]
        print('Number of unique tokens: %d' % len(dictionary))
        print('Number of documents: %d' % len(corpus))
        # Set training parameters.\
        x, y = [], []
        for num_topics in range(5, 40):

            chunksize = 2000
            passes = 20
            iterations = 400
            eval_every = None  # Don't evaluate model perplexity, takes too much time.

            # Make an index to word dictionary.
            temp = dictionary[0]  # This is only to "load" the dictionary.
            id2word = corpora.Dictionary(data_lemetized)

            model = LdaModel(
                corpus=corpus,
                id2word=id2word,
                chunksize=chunksize,
                alpha='auto',
                eta='auto',
                iterations=iterations,
                num_topics=num_topics,
                passes=passes,
                eval_every=eval_every
            )
            #top_topics = model.top_topics(corpus)
            pprint(model.print_topics())
            doc_lda = model[corpus]
            coherence_model_lda = CoherenceModel(model=model, texts=data_lemetized, dictionary=id2word, coherence='c_v')
            coherence_lda = coherence_model_lda.get_coherence()
            x.append(num_topics)
            y.append(coherence_lda)
            #top_topics.show_topics(num_words=5, formatted=False)
            print('\nCoherence Score: ', coherence_lda)
            # Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
            grid = {}
            grid['Validation_Set'] = {}
            # Topics range
            min_topics = 2
            max_topics = 60
            step_size = 1
            topics_range = range(min_topics, max_topics, step_size)
            # Alpha parameter
            alpha = list(np.arange(0.01, 1, 0.3))
            alpha.append('symmetric')
            alpha.append('asymmetric')
            # Beta parameter
            beta = list(np.arange(0.01, 1, 0.3))
            beta.append('symmetric')
            # Validation sets
            num_of_docs = len(corpus)
            corpus_sets = [  # gensim.utils.ClippedCorpus(corpus, num_of_docs*0.25),
                # gensim.utils.ClippedCorpus(corpus, num_of_docs*0.5),
                gensim.utils.ClippedCorpus(corpus, num_of_docs * 0.75),
                corpus]
            corpus_title = ['75% Corpus', '100% Corpus']
            model_results = {'Validation_Set': [],
                             'Topics': [],
                             'Alpha': [],
                             'Beta': [],
                             'Coherence': []
                             }
            # Can take a long time to run
            if 1 == 1:
                pbar = tqdm.tqdm(total=540)

                # iterate through validation corpuses
                for i in range(len(corpus_sets)):
                    # iterate through number of topics
                    for k in topics_range:
                        # iterate through alpha values
                        for a in alpha:
                            # iterare through beta values
                            for b in beta:
                                # get the coherence score for the given parameters
                                cv = compute_coherence_values(corpus=corpus_sets[i], dictionary=id2word,
                                                              k=k, a=a, b=b)
                                # Save the model results
                                model_results['Validation_Set'].append(corpus_title[i])
                                model_results['Topics'].append(k)
                                model_results['Alpha'].append(a)
                                model_results['Beta'].append(b)
                                model_results['Coherence'].append(cv)

                                pbar.update(1)
                pd.DataFrame(model_results).to_csv('lda_tuning_results.csv', index=False)
                pbar.close()
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.plot(x, y)
        plt.xlabel("Number of Topics")
        plt.ylabel("Coherency Score")
        plt.title("Topics vs Coherency with " + str(rank) + " Clusters"  + " in " + subreddit)

        directory = "LDA_Graphs/" + subreddit + "NoDeletedUsers" + "/Topics Vs Coherency " + str(rank)
        plt.savefig(directory)
        plt.close()
    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
