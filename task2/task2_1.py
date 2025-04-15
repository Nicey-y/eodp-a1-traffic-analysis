import pandas as pd
from collections import defaultdict
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# accident = pd.read_csv('accident_subset.csv')

def task2_1():
    accident = pd.read_csv('/course/accident.csv')
    text_columns = ['ACCIDENT_TYPE_DESC', 'DAY_WEEK_DESC', 'DCA_DESC', 'ROAD_GEOMETRY_DESC', 'RMA']

    # convert to lower case

    # def to_lowercase():
    accident[text_columns] = accident[text_columns].apply(lambda x: x.str.lower())
        # accident_no to lower case
    accident['ACCIDENT_NO'] = accident['ACCIDENT_NO'].apply(lambda x: x[0].lower() + x[1:])


    # remove punctuation
    # punctuation = [',','.','!','?','-','(',')','[',']','{','}','\\','//','\\\\','////',
    #       ';',':','~']

    # def remove_punctuation():

    # for mark in punctuation:
    accident = accident.apply(lambda x: x.replace(r'[^A-z\s]',''))


    # remove stop words
    stop_words = set(stopwords.words('english'))
    
    ''' non-accident-related terms
    stop_words = [
        'a', 'an', 'the',
        'in', 'on', 'at', 'with', 'by', 'under', 'over', 'between', 'above', 'beneath',
        'and', 'but', 'or', 'nor', 'for', 'so', 'yet',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
        'very', 'too', 'never', 'always', 'here', 'there',
        'this', 'that', 'these', 'those',
        'all', 'some', 'many', 'few', 'several', 'every',
        'of', 'to', 'as', 'from', 'about', 'on', 'up', 'down', 'out', 'in',
        'far', 'side', 'off', 'from', 'only', 'into', 'while', 'front', 'any', 'away',
        'both', 'opposite', 'single', 'double', 'triple', 'left', 'right', 'not', 'end',
        'u', 'turn', 'other', 'another', 'through', 'no', 'near', 'rear', 'straight',
        'users', 'adjacent', 'median', 'island', 'oppposing', 'furniture', 'temporary',
        'elsewhere', 'classifiable', 'against', 'playing', 'fall', 'same', 'animal'
]
'''
    
    def remove_stop_words(text):
        words = re.findall(r'\b\w+\b', text)

        filtered_text = []
        for word in words:
            filtered_text.append(word if word not in stop_words else '')
        return ' '.join(filtered_text)

    accident = accident.map(lambda x: remove_stop_words(str(x)))

    # word cloud

    most_frequent_words = []
    bag_of_words = defaultdict(int)

    accident['ACCIDENT_TERMS'] = accident['ACCIDENT_TYPE_DESC'] + ' ' + accident['DCA_DESC']

    def update_word_count(text):
        words = re.findall(r'\b\w+\b', text)
        for word in words:
            bag_of_words[word] +=1

    accident['ACCIDENT_TERMS'] = accident['ACCIDENT_TERMS'].apply(lambda x: update_word_count(x))

    bag_of_words = dict(bag_of_words)
    bag_of_words = dict(sorted(bag_of_words.items(), key=lambda item: item[1], reverse=True))

    word_cloud = dict(list(bag_of_words.items())[:20])

    # Step 1: Create the WordCloud object with the frequency dictionary
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_cloud)

    # Step 2: Display the word cloud using matplotlib
    plt.figure(figsize=(10, 5))  # Adjust the size as needed
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Turn off the axis
    plt.savefig('task2_1_word_cloud.png')
