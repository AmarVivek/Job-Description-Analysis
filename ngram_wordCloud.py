from datetime import datetime
import pandas as pd
import nltk
from nltk.corpus import stopwords
import itertools
from wordcloud import WordCloud, STOPWORDS, get_single_color_func
import matplotlib.pyplot as plt
from collections import Counter

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

def n_grams_wordCloud(input_file, encoding, n_filter, n):
    tokens = tokenize(input_file, encoding)
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
    color_to_words = {
        # words below will be colored with a green single color function
        '#00ff00': ['beautiful', 'explicit', 'simple', 'sparse',
                    'readability', 'rules', 'practicality',
                    'explicitly', 'one', 'now', 'easy', 'obvious', 'better'],
        # will be colored with a red single color function
        'red': ['ugly', 'implicit', 'complex', 'complicated', 'nested',
                'dense', 'special', 'errors', 'silently', 'ambiguity',
                'guess', 'hard']
    }

    # Words that are not in any of the color_to_words values
    # will be colored with a grey single color function
    default_color = 'grey'

    # Create a color function with single tone
    # grouped_color_func = SimpleGroupedColorFunc(color_to_words, default_color)

    # Create a color function with multiple tones
    grouped_color_func = GroupedColorFunc(color_to_words, default_color)

    # Apply our color function
    #wc.recolor(color_func=grouped_color_func)
    # plot wordcloud
    fig = plt.figure(figsize=(20, 10), facecolor='k')
    plt.imshow(wc,interpolation="bilinear")
    plt.axis("off")
    plt.draw()
    file_name = "software developer - " + str(n) + " words.png"
    fig.savefig(file_name, facecolor='k', bbox_inches='tight')

if __name__ == "__main__":
    start_time = datetime.now()
    for i in range(1,5):
        print ("Running analysis for " + str(i) +" words!")
        s = n_grams_wordCloud("C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Job Specific/Second Run/software developer.csv",'utf-8', n_filter=10, n=i)
    #n_grams_wordCloud("C:/Users/a.vivek/PycharmProjects/Calgary/ngram2.py",'utf-8', n_filter=2, n=3)
    #with open("output.csv", 'w',newline='') as resultFile:
    #    wr = csv.writer(resultFile, dialect='excel')
    #    wr.writerow(['Ngram_Freq','MI','Ngram_Prob','Count','Ngram'])
    #    wr.writerows(s)
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))