import math
import csv
from datetime import datetime
from collections import Counter
import pandas as pd
import nltk
from nltk.corpus import stopwords
import itertools
from functools import reduce

def text_clean(df_col):
    #  Converting to Lower Case
    df_col = df_col.apply(lambda x: " ".join(x.lower() for x in str(x).split()))
    # Removing Punctuation
    df_col = df_col.str.replace('[^\w\s]', '')

    # Removing Stopwords
    stop = stopwords.words('english')
    df_col = df_col.apply(lambda x: " ".join(x for x in x.split() if x not in stop))

    # Removing unnecessary noise
    removeWords = ['ltbrgtltbrgt', 'ltulgt', 'ltbrgt', 'lt', 'br', 'gt', 'ul', 'be', 'to', 'of', 'with', 'a', 'the',
                   'in', 'for', 'is', 'or', 'on', 'as', 'an', 'be', 'our', 'are']
    df_col = df_col.apply(
        lambda x: " ".join(x for x in x.split() if x not in removeWords))
    return df_col


def tokenize(input_file, encoding):
    tokens = []
    df = pd.read_csv(input_file)
    df['Job_Description'] = text_clean(df['Job_Description'])
    df["unigrams"] = df["Job_Description"].apply(nltk.word_tokenize)
    tokens = list(itertools.chain.from_iterable(df["unigrams"]))
    print (len(tokens))
    return tokens


def ngrams_split(lst, n):
    return [' '.join(lst[i:i+n]) for i in range(len(lst)-n)]

def n_grams_count(tokens, n_filter, n):
    ngram_count = []
    word_count = len(tokens)
    ng2 = ngrams_split(tokens, 2)
    for ngram, count in Counter(ngrams_split(tokens, n)).items():
        if count >= n_filter:
            split = ngram.split()
            ngram_freq = math.log(count/word_count, 10)
            num = count*word_count

            cgrams = [ng2.count(split[i] + ' ' + split[i+1]) for i in range(n-1)]
            freqs = [tokens.count(word) for word in split]
            product = reduce(lambda x, y: x*y, freqs)

            mi = math.pow(math.log(num/(product), 10), 2)

            probs = [cgram/freq for cgram, freq in zip(cgrams, freqs)]
            ngram_prob = sum(math.log(prob, 10) for prob in probs)
            ngram_count.append((ngram_freq, mi, ngram_prob, count, ngram))

    return ngram_count


def n_grams_stat(input_file, encoding, n_filter, n):
    tokens = tokenize(input_file, encoding)
    return n_grams_count(tokens, n_filter, n)


if __name__ == "__main__":
    start_time = datetime.now()
    s = n_grams_stat("C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Job Specific/software developer.csv",'utf-8', n_filter=1, n=2)
    #s = n_grams_stat("C:/Users/a.vivek/PycharmProjects/Calgary/ngram2.py",'utf-8', n_filter=2, n=3)
    with open("output.csv", 'w',newline='') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(['Ngram_Freq','MI','Ngram_Prob','Count','Ngram'])
        wr.writerows(s)
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))