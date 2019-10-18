import pickle
import pandas as pd
import tensorflow as tf
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')

#jobTitlesDF = pd.read_csv("indeedJobsHello.csv", error_bad_lines=False )
#print(jobTitlesDF.shape)
#jobTitlesDF.drop_duplicates(keep='first',inplace=True) #todo repickle this  - so we dont do it each time
#print(jobTitlesDF.shape)
#jobTitlesDF.to_csv('indeedJobsHello.csv',index=False)


#generalJobTitlesDF = pd.read_csv("Job_title.csv")

# print(jobTitlesDF.shape)
# jobTitlesDF.drop_duplicates(keep='first',inplace=True) #todo repickle this  - so we dont do it each time
# jobTitlesDF.to_csv('IndeedJobs.csv')
# print(jobTitlesDF.shape)


def countFreq(list):
    freq = {}
    for i in list:
        if (i in freq):
            freq[i] += 1
        else:
            freq[i] = 1
    return freq

def job_Vec2Categorical(label):
    labels = tf.keras.utils.to_categorical(y=label)
    # print(labels)
    # print(labels.shape)
    return labels

#filesavename(example) = 'mypickle.pkl'
def pickleThis(fileSaveName,obj2Save):
    with open(fileSaveName, 'wb') as pickle_file:
        pickle.dump(obj2Save, pickle_file)
        print('pickled it!')

def unpickleThis(fileSaveName):
    #open pickle
    pickle_in = open(fileSaveName,'rb')
    obj = pickle.load(pickle_in)
    pickle_in.close()
    print('unpickled!')
    return obj

def removeStops(jobTitlesDF):
    stop_words = ["(", ")", "/", ":", ",", "-", "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
                  "you're", "you've", "you'll", "you'd", "your", "yours", "yourself", "yourselves", "he", "him", "his",
                  "himself", "she", "she's", "her", "hers", "herself", "it", "it's", "its", "itself", "they", "them",
                  "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "that'll", "these",
                  "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having",
                  "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until",
                  "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during",
                  "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over",
                  "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all",
                  "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only",
                  "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "don't", "should",
                  "should've", "now", "d", "ll", "m", "o", "re", "ve", "y", "ain", "aren", "aren't", "couldn",
                  "couldn't", "didn", "didn't", "doesn", "doesn't", "hadn", "hadn't", "hasn", "hasn't", "haven",
                  "haven't", "isn", "isn't", "ma", "mightn", "mightn't", "mustn", "mustn't", "needn", "needn't", "shan",
                  "shan't", "shouldn", "shouldn't", "wasn", "wasn't", "weren", "weren't", "won", "won't", "wouldn",
                  "wouldn't"]
    filtered_titles = []
    split_word = ''
    for title in jobTitlesDF['RoleTitle']:
        word_tokens = word_tokenize(title)
        filtered_title = [w for w in word_tokens if w not in stop_words]
        filtered_titles.append(' '.join(filtered_title))

    jobTitlesDF['titlesNoStopWords'] = filtered_titles
    return jobTitlesDF['titlesNoStopWords']

def genLabels(jobTitlesDF,generalJobTitlesDF):
    label = []
    counter = 0
    genJob = generalJobTitlesDF['job_title'].values
    # create labels
    for idx, row in enumerate(jobTitlesDF['RoleTitle']):
        # if (counter == 6): #for testing, print x jobs
        #    break
        # print(idx, ' ---->>>> ', row)


        #jobs_str = jobTitlesDF['RoleTitle'][counter].lower()
        jobs_str = jobTitlesDF['RoleTitle'].iloc[counter].lower()

        # find key words in job title
        if any(title in jobs_str for title in genJob) and (counter not in label):
            title_idx = 2
            for title in genJob:
                if (title in jobs_str):
                    print("found:",title, "[",title_idx,"] -> ",row)
                    break
                title_idx += 1

            label.append(title_idx)
        else:
            #last idx -1
            label.append(124)  # job wasnt found
        counter += 1
    return label

def genLabels2(jobTitlesDF,generalJobTitlesDF):
    label = []
    idxList = []

    genJob = generalJobTitlesDF['job_title'].values
    #genJob = jobTitlesDF
    # create labels
    for idx, row in enumerate(jobTitlesDF['RoleTitle'].str.lower()):
    # if any(title in jobs_str for title in genJob) and (counter not in label):
        if any(title in row for title in genJob):
            title_idx = 2
            for title in genJob:
                if(title in row):
                    label.append(title_idx)
                    break
                title_idx+=1

        else:
            idxList.append(idx)
            label.append(150)
    return label, idxList

# print(jobTitlesDF['RoleTitle'][0:10])
# jobTitlesDF['RoleTitle'] = removeStops(jobTitlesDF)
# print(jobTitlesDF['RoleTitle'][0:10])
#




#label1,delList = genLabels2(jobTitlesDF,generalJobTitlesDF)
# print(label1)
# a = countFreq(label1)
# print(a)

# for i in delList:
#     print(jobTitlesDF['RoleTitle'][i])


# modDF = jobTitlesDF.drop(jobTitlesDF.index[delList[0:17000]])
# modDF.to_csv('indeedJobsTest1.csv',index= False)

#print(jobTitlesDF.shape)


#pickleThis('jobLabels.pkl',label1)
#---------------------------------------------------------------------

#label1 = unpickleThis('jobLabels.pkl')
#print(label1)


#freq = countFreq(label1)
#print(freq)

#aux = [(freq[key], key) for key in freq]
#aux.sort()
#aux.reverse()
#print(aux)


# print(jobTitlesDF['RoleTitle'][20])
# print(label1[20])
#
# text1 = 'Systems Operator'
# str = '25N Nodal Network Systems Operator-Maintainer'
# print(str.find(text1))