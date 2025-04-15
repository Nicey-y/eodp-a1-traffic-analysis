import pandas as pd
from collections import defaultdict
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def task2_1():
    accident = pd.read_csv('accident_subset.csv')
    text_columns = ['ACCIDENT_TYPE_DESC', 'DAY_WEEK_DESC', 'DCA_DESC', 'ROAD_GEOMETRY_DESC', 'RMA']

    # convert column entries with text to lower case
    accident[text_columns] = accident[text_columns].apply(lambda x: x.str.lower())
    
    # accident_no to lower case
    accident['ACCIDENT_NO'] = accident['ACCIDENT_NO'].apply(lambda x: x[0].lower() + x[1:])

    # remove punctuation
    accident = accident.apply(lambda x: x.replace(r'[^A-z\s]',''))

    # remove stop words
    stop_words = set(stopwords.words('english'))
    
    
    def remove_stop_words(text):
        words_in_text = re.findall(r'\b\w+\b', text)
        filtered_text = []
        for word in words_in_text:
            filtered_text.append(word if word not in stop_words else '')
        return ' '.join(filtered_text)

    # removes stop words from the dataframe if entry is a string
    accident = accident.map(lambda x: remove_stop_words(str(x)))

    ###################################################################################################################
    
    # word cloud

    most_frequent_words = []
    bag_of_words = defaultdict(int)

    accident['ACCIDENT_TERMS'] = accident['ACCIDENT_TYPE_DESC'] + ' ' + accident['DCA_DESC']

    # find frequencies of all occurrences of each word
    def update_word_count(text):
        words_in_text = re.findall(r'\b\w+\b', text)
        for word in words_in_text:
            bag_of_words[word] +=1

    accident['ACCIDENT_TERMS'] = accident['ACCIDENT_TERMS'].apply(lambda x: update_word_count(x))

    bag_of_words = dict(bag_of_words)
    # sort acc. to most occurring word to least
    bag_of_words = dict(sorted(bag_of_words.items(), key=lambda item: item[1], reverse=True))

    # 20 most frequent words
    word_cloud = dict(list(bag_of_words.items())[:20])

    # create wordcloud with word_cloud dict
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_cloud)

    # display wordcloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('task2_1_word_cloud.png')
