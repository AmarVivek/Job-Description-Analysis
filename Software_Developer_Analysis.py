from collections import Counter # Keep track of our term counts
import pandas as pd # For converting results to a dataframe and bar chart plots
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
import os
import lda
import matplotlib as mpl
from subprocess import check_output

def text_cleaner(job_description):

    text = job_description  # Get the text from this
    lines = (line.strip() for line in text.splitlines())  # break into lines
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))  # break multi-headlines into a line each
    def chunk_space(chunk):
        chunk_out = chunk + ' '  # Need to fix spacing issue
        return chunk_out
    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode(
        'utf-8')  # Get rid of all blank lines and ends of line
    text = text.lower().split()  # Go to lower case and split them apart
    text = list(
        set(text))  # Last, just get the set of these. Ignore counts (we are just looking at whether a term existed)
    return text

job_descriptions=[]
df = pd.read_csv("C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Job Specific/Second Run/software developer.csv")
#  Converting to Lower Case
df['Job_Description'] = df['Job_Description'].apply(lambda x: " ".join(x.lower() for x in str(x).split()))
# Removing Punctuation
df['Job_Description'] = df['Job_Description'].str.replace('[^\w\s]','')

# Removing Stopwords
stop = stopwords.words('english')
df['Job_Description'] = df['Job_Description'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))

# Removing unnecessary noise
removeWords = ['ltbrgtltbrgt', 'ltdivgt', 'ltulgt', 'ltbrgt', 'lt', 'br', 'gt', 'ul', 'be', 'to', 'of', 'with', 'a', 'the', 'years', 'des', 'toronto','eg', 'etc','de','et',
               'in', 'for', 'is', 'or', 'on', 'as', 'an', 'be', 'our', 'are', 'calgary', 'systemscanada', 'markit', 'ihs',
               'et', 'des','la','Ã', 'youll', 'like', 'etc','en','de','les',
               ## Entered by Me!!
               'application', 'sales', 'help', 'well', 'mobile', 'oil', 'asset',
               'skills', 'solutions', 'knowledge', 'including', 'code', 'us', 'back',
               'work', 'systems', 'strong', 'industry', 'looking', 'customers', 'needs',
               'jobs', 'must', 'user', 'analyst', 'service', 'activities', 'banking',
               'experience', 'engineering', 'computer', 'understanding', 'products', 'applicants', 'general',
               'business', 'new', 'client', 'customer', 'control', 'employees',
               'support', 'working', 'years', 'please', 'ensure', 'existing', 'also',
               'environment', 'requirements', 'amp', 'develop', 'tools', 'process', 'best',
               'developer', 'clients', 'professional', 'processes', 'performance', 'degree', 'andor',
               'job', 'technology', 'using', 'make', 'standards', 'benefits', 'implementation',
               'ltligtexperience', 'maintain', 'take', 'share', 'qualifications', 'building',
               'management', 'developing', 'ltstronggt', 'deliver', 'alberta',
               'software', 'projects', 'opportunity', 'join', '5', 'practices', 'excellent',
               'team', 'see', 'part', 'integration', 'create', 'developers', 'security',
               'technical', 'services', 'people', 'test', 'product', 'within', 'canada',
               'applications', 'type', 'programming', 'one', 'location', 'advertiser', 'posted',
               'project', 'information', 'position', 'role', 'provide', 'manager', 'area',
               'development', 'web', 'system', 'ability', 'communication', 'quality', 'learning',
               'design', 'technologies', 'based', 'testing', 'related', 'time', 'plans',
               'company', 'opportunities', 'required', 'written', 'may', 'category', 'agile',
               'maritime', '10', 'canada', 'canadian',' endlessthe', '8', '10', 'however', 'highlycomplex', 'thank', 'interest', 'per', 'solium', 'reward', 'proud', 'canadas', '1100', 'endlessthe',
                'airborne', 'maritime', 'valid', 'conscientious', 'dynamics', 'ltligt', '3', '10', '8', '3', '2', '1', 'dynamics', 'candidate', 'bachelors', 'ltpgt', 'employ', 'projectprogram', 'workplaceworkplace',
                'ltligtyou', 'sexual', 'obtainhold']
df['Job_Description'] = df['Job_Description'].apply(lambda x: " ".join(x for x in x.split() if x not in removeWords))

#one_line = " ".join(df['Job_Description'])

more_freq = pd.Series(' '.join(df['Job_Description']).split()).value_counts()[:20]
print (more_freq)
for job_text in df['Job_Description']:
    final_description = text_cleaner(job_text)
    if final_description:  # So that we only append when the website was accessed correctly
        job_descriptions.append(final_description)

print ('There were', len(job_descriptions), 'jobs successfully found.')

doc_frequency = Counter()  # This will create a full counter of our terms.
[doc_frequency.update(item) for item in job_descriptions]

word_counts_df = pd.DataFrame.from_dict(dict(doc_frequency), orient='index')
word_counts_df.to_csv("word_count_SD.csv")

prog_lang_dict = Counter({'R': doc_frequency[b'r'], 'Python': doc_frequency[b'python'],
                          'Java': doc_frequency[b'java'], 'C++': doc_frequency[b'c++'], 'Mainframe': doc_frequency[b'mainframes'],
                          'Ruby': doc_frequency[b'ruby'], 'Informatica' : doc_frequency[b'informatica'],
                          'Perl': doc_frequency[b'perl'], 'Matlab': doc_frequency[b'matlab'],
                          'JavaScript': doc_frequency[b'javascript'], 'Scala': doc_frequency[b'scala'],
                          'Android': doc_frequency[b'android'], 'Asp.Net': doc_frequency[b'aspnet'], 'C': doc_frequency[b'c'],
                          'HTML': doc_frequency[b'html'], 'Swift': doc_frequency[b'swift']})

tool_dict = Counter({'Excel': doc_frequency[b'excel'], 'Tableau': doc_frequency[b'tableau'],
                              'D3.js': doc_frequency[b'd3.js'], 'SAS': doc_frequency[b'sas'],
                              'SPSS': doc_frequency[b'spss'], 'D3': doc_frequency[b'd3'], 'GitHub': doc_frequency[b'git'], 'SAP': doc_frequency[b'sap']})

framework_dict = Counter({'Hadoop': doc_frequency[b'hadoop'], 'MapReduce': doc_frequency[b'mapreduce'],
                       'Spark': doc_frequency[b'spark'], 'Pig': doc_frequency[b'pig'],
                       'Hive': doc_frequency[b'hive'], 'Shark': doc_frequency[b'shark'],
                       'Oozie': doc_frequency[b'oozie'], 'ZooKeeper': doc_frequency[b'zookeeper'],
                       'Flume': doc_frequency[b'flume'], 'Mahout': doc_frequency[b'mahout'], 'Linux': doc_frequency[b'linux'],
                        'UI': doc_frequency[b'ui'], 'AI': doc_frequency['ai'], 'UX': doc_frequency[b'ux'], 'AWS': doc_frequency[b'aws'],
                        'Apache': doc_frequency[b'apache']})

database_dict = Counter({'SQL': doc_frequency[b'sql'], 'NoSQL': doc_frequency[b'nosql'],
                         'HBase': doc_frequency[b'hbase'], 'Cassandra': doc_frequency[b'cassandra'],
                         'MongoDB': doc_frequency[b'mongodb'], 'DB2': doc_frequency[b'db2']})

process_dict = Counter({'Cloud': doc_frequency[b'cloud'], 'Agile': doc_frequency[b'agile'], 'Microsoft': doc_frequency[b'microsoft'],
                        'DevOps': doc_frequency[b'devops']})

overall_total_skills = prog_lang_dict + tool_dict + framework_dict + database_dict + process_dict  # Combine our Counter objects

final_frame = pd.DataFrame.from_dict(overall_total_skills, orient='index')
final_frame.reset_index(level=0, inplace=True)
final_frame.columns = ['Term', 'NumPostings']
# dataframe
print (final_frame)
# Change the values to reflect a percentage of the postings

final_frame.NumPostings = (final_frame.NumPostings) * 100 / len(job_descriptions)  # Gives percentage of job postings
#  having that term

# Sort the data for plotting purposes

final_frame.sort_values(by=['NumPostings'], ascending=False, inplace=True)

# Get it ready for a bar plot

fig = final_frame.plot(x='Term', kind='bar', legend=None, title='Percentage of Software Developer Job Ads with a Key Skill',fontsize=6.5)
plt.ylabel('Percentage Appearing in Job Ads')
plt.show()