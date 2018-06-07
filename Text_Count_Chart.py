from bs4 import BeautifulSoup # For HTML parsing
import re # Regular expressions
from time import sleep # To prevent overwhelming the server between connections
from collections import Counter # Keep track of our term counts
import pandas as pd # For converting results to a dataframe and bar chart plots
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import wikipedia
from wordcloud import WordCloud, STOPWORDS
import os

def text_cleaner(job_description):

    text = job_description  # Get the text from this

    lines = (line.strip() for line in text.splitlines())  # break into lines

    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))  # break multi-headlines into a line each

    def chunk_space(chunk):
        chunk_out = chunk + ' '  # Need to fix spacing issue
        return chunk_out

    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode(
        'utf-8')  # Get rid of all blank lines and ends of line

    # Now clean out all of the unicode junk (this line works great!!!)

    #try:
     #   text = text.decode('unicode_escape').encode('ascii', 'ignore')  # Need this as some websites aren't formatted
    #except:  # in a way that this works, can occasionally throw
      #  return  # an exception

    #text = re.sub("[^a-zA-Z.+3]", " ", text)  # Now get rid of any terms that aren't words (include 3 for d3.js)
    # Also include + for C++

    text = text.lower().split()  # Go to lower case and split them apart

    stop_words = set(stopwords.words("english"))  # Filter out any stop words
    text = [w for w in text if not w in stop_words]

    text = list(
        set(text))  # Last, just get the set of these. Ignore counts (we are just looking at whether a term existed
    # or not on the website)

    return text

job_descriptions=[]
df = pd.read_csv("C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Job Specific/data scientist.csv")
for job_text in df['Job_Description']:
    final_description = text_cleaner(job_text)
    if final_description:  # So that we only append when the website was accessed correctly
        job_descriptions.append(final_description)

#print (job_descriptions)

print ('There were', len(job_descriptions), 'jobs successfully found.')

doc_frequency = Counter()  # This will create a full counter of our terms.
[doc_frequency.update(item) for item in job_descriptions]  # List comp
# Now we can just look at our final dict list inside doc_frequency

# Obtain our key terms and store them in a dict. These are the key data science skills we are looking for

prog_lang_dict = Counter({'R': doc_frequency[b'r'], 'Python': doc_frequency[b'python'],
                          'Java': doc_frequency[b'java'], 'C++': doc_frequency[b'c++'],
                          'Ruby': doc_frequency[b'ruby'],
                          'Perl': doc_frequency[b'perl'], 'Matlab': doc_frequency[b'matlab'],
                          'JavaScript': doc_frequency[b'javascript'], 'Scala': doc_frequency[b'scala']})

analysis_tool_dict = Counter({'Excel': doc_frequency[b'excel'], 'Tableau': doc_frequency[b'tableau'],
                              'D3.js': doc_frequency[b'd3.js'], 'SAS': doc_frequency[b'sas'],
                              'SPSS': doc_frequency[b'spss'], 'D3': doc_frequency[b'd3']})

hadoop_dict = Counter({'Hadoop': doc_frequency[b'hadoop'], 'MapReduce': doc_frequency[b'mapreduce'],
                       'Spark': doc_frequency[b'spark'], 'Pig': doc_frequency[b'pig'],
                       'Hive': doc_frequency[b'hive'], 'Shark': doc_frequency[b'shark'],
                       'Oozie': doc_frequency[b'oozie'], 'ZooKeeper': doc_frequency[b'zookeeper'],
                       'Flume': doc_frequency[b'flume'], 'Mahout': doc_frequency[b'mahout']})

database_dict = Counter({'SQL': doc_frequency[b'sql'], 'NoSQL': doc_frequency[b'nosql'],
                         'HBase': doc_frequency[b'hbase'], 'Cassandra': doc_frequency[b'cassandra'],
                         'MongoDB': doc_frequency[b'mongodb']})

overall_total_skills = prog_lang_dict + analysis_tool_dict + hadoop_dict + database_dict  # Combine our Counter objects

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

fig = final_frame.plot(x='Term', kind='bar', legend=None, title='Percentage of Data Scientist Job Ads with a Key Skill')
plt.ylabel('Percentage Appearing in Job Ads')
#fig.savefig
#fig = final_plot.get_figure()  # Have to convert the pandas plot object to a matplotlib object
#fig
plt.show()

def create_wordcloud(text):
    #mask = np.array(Image.open(os.path.join(currdir, "cloud.png")))
    stopwords = set(STOPWORDS)
    wc = WordCloud(background_color="white",
    #               mask=mask,
                   max_words=200,
                   stopwords=stopwords)
    wc.generate(text)
    wc.to_file(os.path.join("Data Scientist.png"))

create_wordcloud(job_descriptions)








