# Adapted from: github.com/aneesha/RAKE/rake.py
from __future__ import division
import operator
import nltk
import string
from pprint import pprint
import pandas as pd
import itertools
from os import walk
from datetime import datetime

def isPunct(word):
    return len(word) == 1 and word in string.punctuation


def isNumeric(word):
    try:
        float(word) if '.' in word else int(word)
        return True
    except ValueError:
        return False


class RakeKeywordExtractor:

    def __init__(self):
        self.stopwords = set(nltk.corpus.stopwords.words())
        self.top_fraction = 1  # consider top third candidate keywords by score

    def _generate_candidate_keywords(self, sentences):
        phrase_list = []
        for sentence in sentences:
            words = map(lambda x: "|" if x in self.stopwords else x,
                        nltk.word_tokenize(sentence.lower()))
            phrase = []
            for word in words:
                if word == "|" or isPunct(word):
                    if len(phrase) > 0:
                        phrase_list.append(phrase)
                        phrase = []
                else:
                    phrase.append(word)
        return phrase_list

    def _calculate_word_scores(self, phrase_list):
        word_freq = nltk.FreqDist()
        word_degree = nltk.FreqDist()
        for phrase in phrase_list:
            degree = len(list(filter(lambda x: not isNumeric(x), phrase))) - 1
            for word in phrase:
                word_freq.update([word])
                word_degree.update([word, degree])  # other words
        for word in word_freq.keys():
            word_degree[word] = word_degree[word] + word_freq[word]  # itself
        # word score = deg(w) / freq(w)
        word_scores = {}
        for word in word_freq.keys():
            word_scores[word] = word_degree[word] / word_freq[word]
        return word_scores

    def _calculate_phrase_scores(self, phrase_list, word_scores):
        phrase_scores = {}
        for phrase in phrase_list:
            phrase_score = 0
            for word in phrase:
                phrase_score += word_scores[word]
            phrase_scores[" ".join(phrase)] = phrase_score
        return phrase_scores

    def extract(self, text, incl_scores=False):
        sentences = nltk.sent_tokenize(text)
        phrase_list = self._generate_candidate_keywords(sentences)
        word_scores = self._calculate_word_scores(phrase_list)
        phrase_scores = self._calculate_phrase_scores(
            phrase_list, word_scores)
        sorted_phrase_scores = sorted(phrase_scores.items(),
                                      key=operator.itemgetter(1), reverse=True)
        n_phrases = len(sorted_phrase_scores)
        if incl_scores:
            return sorted_phrase_scores[0:int(n_phrases / self.top_fraction)]
        else:
            return map(lambda x: x[0],
                       sorted_phrase_scores[0:int(n_phrases / self.top_fraction)])

def get_file_names(file_path):
    f=[]
    for (dirpath, dirnames, filenames) in walk(file_path):
        f.extend(filenames)
    return f

def get_keywords(in_file_path, out_file_path, file_name):
    rake = RakeKeywordExtractor()
    in_file = in_file_path + "/" + file_name
    data = pd.read_csv(in_file)
    data = data.drop_duplicates(subset=['Job_Description'])
    text = data["Job_Description"]
    ab = str(list(itertools.chain(text)))
    keywords = rake.extract(ab,incl_scores=True)
    out_file = out_file_path + "/" + file_name
    with open(out_file, mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(str(line) for line in keywords))


if __name__ == "__main__":
    start_time = datetime.now()
    in_file_path = "C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Job Specific/Second Run"
    out_file_path = "C:/Users/a.vivek/Desktop/Projects/Calgary/Analysis/Text Summarization"
    file_name_list = get_file_names(in_file_path)
    for file_name in file_name_list:
        print ("Processing for " + str(file_name))
        get_keywords(in_file_path, out_file_path, file_name)
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))