import pandas as pd
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
from textblob import Word
import numpy as np
run = "Second Run"
df_indeed = pd.read_csv("C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Indeed_Project_withJDAll.csv")
df_stackOverflow = pd.read_csv('C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/StackOverflow_Project_withJD.csv')
df_glassDoor = pd.read_csv('C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Glassdoor_Project_withJD.csv')
df_calgaryJobBoard = pd.read_csv('C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/CalgaryJobBoard_Project_withJD.csv')
df_indeed_national = pd.read_csv('C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Indeed_Project_withJDAll_National.csv')
df_glassdoor_national = pd.read_csv('C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Glassdoor_Project_withJD_National.csv')

df_all = pd.concat([df_indeed, df_stackOverflow, df_glassDoor, df_calgaryJobBoard, df_glassdoor_national, df_indeed_national])
df_all = df_all.reset_index(drop=True)

print ("Length of Indeed postings : " + str(len(df_indeed) + len(df_indeed_national)))
print ("Length of StackOverFlow postings : " + str(len(df_stackOverflow)))
print ("Length of GlassDoor postings : " + str(len(df_glassDoor) + len(df_glassdoor_national)))
print ("Length of Calgary Job Board postings : " + str(len(df_calgaryJobBoard)))
print ("Length of All postings : " + str(len(df_all)))

# Cleaning the "+" and "-" from within the Job Types
df_all['Job Type'] = df_all['Job Type'].apply(lambda x: x.replace('+',' '))
df_all['Job Type'] = df_all['Job Type'].apply(lambda x: x.replace('-',' '))
df_all['Job Type'] = df_all['Job Type'].apply(lambda x: x.replace('fullstack','full stack'))
df_all['Job Type'] = df_all['Job Type'].apply(lambda x: x.replace('cybersecurity','cyber security'))

df = df_all.groupby('Job Type').count()

df.to_csv('Counts of Jobs.csv', encoding='utf-8')

def write_file_role(role, df_input):
    df_role = df_input.loc[(df_input['Job Type'] == role)]
    df_role =  df_role.loc[~pd.isna(df_role['Job_Description'])]
    file_path = 'C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Job Specific/' + run + "/" + role + '.csv'
    df_role.to_csv(file_path, encoding='utf-8')
    print ("For " + role + ", " + str(len(df_role)) + " jobs were written!")

for role in df_all['Job Type'].unique():
    write_file_role(role, df_all)