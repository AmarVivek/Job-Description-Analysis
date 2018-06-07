'''
import numpy as np
import lda
import lda.datasets

X = lda.datasets.load_reuters()
vocab = lda.datasets.load_reuters_vocab()
titles = lda.datasets.load_reuters_titles()

model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
model.fit(X)
topic_word = model.topic_word_
n_top_words = 8
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
    print ('Topic {} : {}'.format(i, ' '.join(topic_words)))
'''

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import itertools
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import numpy as np

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
                   'in', 'for', 'is', 'or', 'on', 'as', 'an', 'be', 'our', 'are', 'calgary', 'systemscanada', 'markit', 'ihs']
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
    #with open(input_file, 'r', encoding=encoding) as f:
    #    for line in f:
    #        words = re.findall('\w+', line.lower())
    #        tokens.extend(words)
    return tokens

def display_topics(H, W, feature_names, documents, no_top_words, no_top_documents):
    for topic_idx, topic in enumerate(H):
        print ("Topic :" + str((topic_idx)))
        print (" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))
        top_doc_indices = np.argsort( W[:,topic_idx] )[::-1][0:no_top_documents]
        for doc_index in top_doc_indices:
            print (documents[doc_index])

# list for tokenized documents in loop
texts = []
doc_set = tokenize("C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Job Specific/Second Run/software developer.csv",'utf-8')
# loop through document list
for i in doc_set:
    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stop = stopwords.words('english')
    stopped_tokens = [i for i in tokens if not i in stop]

    # stem tokens
    #stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

    # add tokens to list
    texts.append(stopped_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=20, id2word=dictionary, passes=20)
print(ldamodel.print_topics(num_topics=20, num_words=7))

for i in  ldamodel.show_topics():
    print (i[0], i[1])
print ("Second Attempt at Printing!")

no_topics = 2
# LDA can only use raw term counts for LDA because it is a probabilistic graphical model
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
tf = tf_vectorizer.fit_transform(corpus)
tf_feature_names = tf_vectorizer.get_feature_names()

# Run LDA
lda_model = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
lda_W = lda_model.transform(tf)
lda_H = lda_model.components_

no_top_words = 4
no_top_documents = 4
display_topics(lda_H, lda_W, tf_feature_names, corpus, no_top_words, no_top_documents)