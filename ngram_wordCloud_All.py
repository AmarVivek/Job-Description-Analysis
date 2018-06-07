import csv
import re
from datetime import datetime
import pandas as pd
import nltk
from nltk.corpus import stopwords
import itertools
import matplotlib as mlp
from wordcloud import WordCloud, STOPWORDS, get_single_color_func
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from os import walk

class SimpleGroupedColorFunc(object):
    """Create a color function object which assigns EXACT colors
       to certain words based on the color to words mapping
       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.
       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)


class GroupedColorFunc(object):
    """Create a color function object which assigns DIFFERENT SHADES of
       specified colors to certain words based on the color to words mapping.
       Uses wordcloud.get_single_color_func
       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.
       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]

        self.default_color_func = get_single_color_func(default_color)

    def get_color_func(self, word):
        """Returns a single_color_func associated with the word"""
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func

        return color_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)

def text_clean(df_col):
    #  Converting to Lower Case
    df_col = df_col.apply(lambda x: " ".join(x.lower() for x in str(x).split()))
    # Removing Punctuation
    df_col = df_col.str.replace('[^\w\s]', '')

    # Removing Stopwords
    stop = stopwords.words('english')
    df_col = df_col.apply(lambda x: " ".join(x for x in x.split() if x not in stop))

    # Removing unnecessary noise
    removeWords = ['ltbrgtltbrgt', 'ltdivgt', 'ltulgt', 'ltbrgt', 'lt', 'br', 'gt', 'ul', 'be', 'to', 'of', 'with', 'a', 'the', 'years', 'des', 'toronto','eg', 'etc','de','et',
                   'in', 'for', 'is', 'or', 'on', 'as', 'an', 'be', 'our', 'are', 'calgary', 'systemscanada', 'markit', 'ihs',
                   'et', 'des','la','Ã', 'youll', 'like', 'etc','en','de','les']
    df_col = df_col.apply(
        lambda x: " ".join(x for x in x.split() if x not in removeWords))
    return df_col


def tokenize(input_file, encoding):
    tokens = []
    df = pd.read_csv(input_file)
    df['Job_Description'] = text_clean(df['Job_Description'])
    df["unigrams"] = df["Job_Description"].apply(nltk.word_tokenize)
    tokens = list(itertools.chain.from_iterable(df["unigrams"]))
    #with open(input_file, 'r', encoding=encoding) as f:
    #    for line in f:
    #        words = re.findall('\w+', line.lower())
    #        tokens.extend(words)
    return tokens


def ngrams_split(lst, n):
    return [' '.join(lst[i:i+n]) for i in range(len(lst)-n)]

# count word occurance
def count_word_occurance(input_words_list):
    word_counts = Counter(input_words_list)
    # returns a dataframe
    word_counts_df = pd.DataFrame.from_dict(dict(word_counts), orient='index')
    word_counts_df.columns = ['count']
    return word_counts_df.sort_values(by='count', ascending=0)

def n_grams_wordCloud(in_file_path, file_name, out_file_path,  encoding, n_filter, n):
    in_file = in_file_path + "/" + file_name
    tokens = tokenize(in_file, encoding)
    ngrams =  ngrams_split(tokens, n)
    stopwords = set(STOPWORDS)
    if n==1:
        maxwords=500
    else:
        maxwords=200

    wc = WordCloud(max_words=maxwords, width=1600, height=800,
                   background_color="white",
                   margin=10,
                   prefer_horizontal=1.0,max_font_size=40)

    # words and plot sizes (word count, relevance, etc)
    word_count = count_word_occurance(ngrams)
    wc.generate_from_frequencies(word_count.to_dict()[word_count.columns[0]])
    fig = plt.figure(figsize=(20, 10), facecolor='k')
    plt.imshow(wc,interpolation="bilinear")
    plt.axis("off")
    plt.draw()
    out_file_name = file_name.split(".")[0] + " - " + str(n) + " words.png"
    out_file = out_file_path + "/" + out_file_name
    fig.savefig(out_file, facecolor='k', bbox_inches='tight')

def get_file_names(file_path):
    f=[]
    for (dirpath, dirnames, filenames) in walk(file_path):
        f.extend(filenames)
    return f

def get_word_cloud(in_file_path, out_file_path, file_name):
    for i in range(1,5):
        print ("Running analysis for " + str(i) +" words!")
        s = n_grams_wordCloud(in_file_path, file_name, out_file_path,'utf-8', n_filter=10, n=i)
    return


if __name__ == "__main__":
    start_time = datetime.now()
    in_file_path = "C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Job Specific/Second Run"
    out_file_path = "C:/Users/a.vivek/Desktop/Projects/Calgary/Analysis/Word Clouds"
    file_name_list = get_file_names(in_file_path)
    for file_name in file_name_list:
        print ("Processing for " + str(file_name))
        get_word_cloud(in_file_path, out_file_path, file_name)
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))