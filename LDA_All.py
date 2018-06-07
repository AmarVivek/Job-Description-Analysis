from datetime import datetime

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import itertools
import pandas as pd
import nltk
from os import walk

tokenizer = RegexpTokenizer(r'\w+')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

def text_clean(df_col):
    #  Converting to Lower Case
    df_col = df_col.apply(lambda x: " ".join(x.lower() for x in str(x).split()))
    # Removing Punctuation
    df_col = df_col.str.replace('[^\w\s]', '')

    # Removing Stopwords
    stop = stopwords.words('english')
    df_col = df_col.apply(lambda x: " ".join(x for x in x.split() if x not in stop))

    # Removing unnecessary noise
    removeWords = ['ltbrgtltbrgt', 'ltdivgt', 'ltulgt', 'ltbrgt', 'lt', 'br', 'gt', 'ul', 'be', 'to', 'of', 'with', 'a', 'the',
                   'in', 'for', 'is', 'or', 'on', 'as', 'an', 'be', 'our', 'are', 'calgary', 'systemscanada', 'markit', 'ihs',
                   'et', 'des','la','Ã', 'youll', 'like', 'etc','en','de','les']
    df_col = df_col.apply(
        lambda x: " ".join(x for x in x.split() if x not in removeWords))
    return df_col


def tokenize(input_file, encoding):
    df = pd.read_csv(input_file)
    df = df.drop_duplicates(subset=['Job_Description'])
    df['Job_Description'] = text_clean(df['Job_Description'])
    df["unigrams"] = df["Job_Description"].apply(nltk.word_tokenize)
    tokens = list(itertools.chain.from_iterable(df["unigrams"]))
    print (len(tokens))
    return tokens


def get_file_names(file_path):
    f=[]
    for (dirpath, dirnames, filenames) in walk(file_path):
        f.extend(filenames)
    return f


def get_topics(in_file_path, out_file_path, file_name):
    in_file = in_file_path + "/" + file_name
    texts = []
    doc_set = tokenize(in_file, 'utf-8')
    for i in doc_set:
        # clean and tokenize document string
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)

        # remove stop words from tokens
        stop = stopwords.words('english')
        stopped_tokens = [i for i in tokens if not i in stop]
        texts.append(stopped_tokens)
    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]
    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=20, id2word=dictionary, passes=20)
    topics = ldamodel.print_topics(num_topics=20, num_words=7)
    out_file = out_file_path + "/" + file_name
    with open(out_file, mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(str(line) for line in topics))


if __name__ == "__main__":
    start_time = datetime.now()
    in_file_path = "C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Job Specific/Second Run"
    out_file_path = "C:/Users/a.vivek/Desktop/Projects/Calgary/Analysis/LDA"
    file_name_list = get_file_names(in_file_path)
    for file_name in file_name_list:
        print ("Processing for " + str(file_name))
        get_topics(in_file_path, out_file_path, file_name)
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))