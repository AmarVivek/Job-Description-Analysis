import pandas as pd
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
from textblob import Word
import numpy as np

df_indeed = pd.read_csv("C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Indeed_Project_withJDAll.csv")
df_stackOverflow = pd.read_csv('C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/StackOverflow_Project_withJD.csv')
df_glassDoor = pd.read_csv('C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Glassdoor_Project_withJD.csv')
df_calgaryJobBoard = pd.read_csv('C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/CalgaryJobBoard_Project_withJD.csv')
df_indeed_national = pd.read_csv('C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Indeed_Project_withJDAll_National.csv')
df_glassdoor_national = pd.read_csv('C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Glassdoor_Project_withJD_National.csv')

df_all = pd.concat([df_indeed, df_stackOverflow, df_glassDoor, df_calgaryJobBoard, df_indeed_national, df_glassdoor_national])

print ("Length of Indeed postings : " + str(len(df_indeed) + len(df_indeed_national)))
print ("Length of StackOverFlow postings : " + str(len(df_stackOverflow)))
print ("Length of GlassDoor postings : " + str(len(df_glassDoor) + len(df_glassdoor_national)))
print ("Length of Calgary Job Board postings : " + str(len(df_calgaryJobBoard)))
print ("Length of All postings : " + str(len(df_all)))

# Cleaning the "+" and "-" from within the Job Types
df_all['Job Type'] = df_all['Job Type'].apply(lambda x: x.replace('+',' '))
df_all['Job Type'] = df_all['Job Type'].apply(lambda x: x.replace('-',' '))

# Calculating Word Count
df_all['Word_Count'] = df_all['Job_Description'].apply(lambda x: len(str(x).split(" ")))

#  Converting to Lower Case
df_all['Job_Description'] = df_all['Job_Description'].apply(lambda x: " ".join(x.lower() for x in str(x).split()))

# Calculating StopWord Count
stop = stopwords.words('english')
df_all['Stopwords_Count'] = df_all['Job_Description'].apply(lambda x: len([x for x in str(x).split() if x in stop]))

# Calculating Specialword Count
df_all['Special_word_count'] = df_all['Job_Description'].apply(lambda x: len([x for x in str(x).split() if x.startswith("/")]))
#print (df_all[['Job_Description','Special_word_count']].head())

#Calculating numerics
df_all['Number_count'] = df_all['Job_Description'].apply(lambda x: len([x for x in str(x).split() if x.isdigit()]))

# Removing Punctuation
df_all['Job_Description'] = df_all['Job_Description'].str.replace('[^\w\s]','')

# Removing Stopwords
df_all['Job_Description'] = df_all['Job_Description'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
#print (df_all['Job_Description'].head())

# Removing unnecessary noise
removeWords = ['ltbrgtltbrgt', 'ltulgt','ltbrgt','lt','br','gt','ul']
df_all['Job_Description'] = df_all['Job_Description'].apply(lambda x: " ".join(x for x in x.split() if x not in removeWords))

# Checking frequently occurring words
more_freq = pd.Series(' '.join(df_all['Job_Description']).split()).value_counts()[:10]

# Tokenization
#print (TextBlob(df_all['Job_Description']).words)

# Stemming
#st = PorterStemmer()
#df_all['Job_Description'][:5].apply(lambda x: " ".join([st.stem(word) for word in x.split()]))

#Lemmatization
df_all['Job_Description'] = df_all['Job_Description'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
#print (df_all['Job_Description'].head())

# N-gram Analysis
#print (TextBlob(df_all['Job_Description'][0]).ngrams(2))

# Term Frequency
tf1 = (df_all['Job_Description'][1:2]).apply(lambda x: pd.value_counts(x.split(" "))).sum(axis = 0).reset_index()
tf1.columns = ['words','tf']
print ("Term Frequency: ", tf1)

# Inverse Document Frequency
for i,word in enumerate(tf1['words']):
    #tf1.loc[i, 'idf'] = np.log(df_all['Job_Description'].shape[0]/(len(df_all[df_all['Job_Description']].str.contains(word)])))
    tf1.loc[i, 'idf'] = np.log(df_all['Job_Description'].shape[0]/(len(df_all[df_all['Job_Description'].str.contains(word)])))
print ("Inverse Document Frequency : ", tf1)

# TF-IDF

tf1['tfidf'] = tf1['tf'] * tf1['idf']
print ("TF-IDF : ", tf1)