import pandas as pd
import re
import matplotlib.pyplot as plt

def task2_2():
    accident = pd.read_csv("a1-datasets/accident.csv")

    accident_times = accident['ACCIDENT_TIME']

    accident['TIME_OF_DAY'] = accident['ACCIDENT_TIME'].apply(lambda x: sort_time(x))

    time_occurrences = {}

    for time in accident['TIME_OF_DAY']:
        if time not in time_occurrences:
            time_occurrences[time] = 1
        else:
            time_occurrences[time] += 1

    time_occurrences_df = pd.DataFrame(list(time_occurrences.items()), columns = ['TIME_OF_DAY', 'ACCIDENT_FREQUENCY'])

    time_occurrences_df = time_occurrences_df.set_index('TIME_OF_DAY')
    time_occurrences_df = time_occurrences_df.reindex(index=['Morning', 'Afternoon', 'Evening', 'Late Night'])

    # bar chart
    plt.title("Number of accidents by Time of Day")
    plt.bar(time_occurrences_df['TIME_OF_DAY'], time_occurrences_df['ACCIDENT_FREQUENCY'])
    plt.xticks(rotation=30)
    plt.savefig('task2_2_timeofday.png')

    # pie charts

    words = {}
    dca_desc_words = []

    for time in time_occurrences_df['TIME_OF_DAY']:
        for desc in accident['DCA_DESC']:

            desc_split = re.findall(r'\b\w+\b', desc) # tokenize words

            for word in desc_split:
                if word not in words:
                    words[word] = 1
                else:
                    words[word] += 1
        
        # arrange acc. to most frequently occurring words
        words_sorted = sorted(list(words.items()), key=lambda x: x[1], reverse=True)
        
        # store 10 most frequent words
        dca_desc_words.append(words_sorted[:10])
        words = {}

    dca_desc_words_rearrange = []
    for ls in dca_desc_words:
        rearrange = list(map(list, zip(*ls)))
        dca_desc_words_rearrange.append(rearrange)
    
    titles = ['Morning', 'Afternoon', 'Evening', 'Late Night']
    fig, axs = plt.subplots(2, 2)
    fig.suptitle('10 most frequent accident terms by time of day')
    for i in range(2):
        for j in range(2):
            index = i * 2 + j
            axs[i, j].pie(dca_desc_words_rearrange[index][1], labels=dca_desc_words_rearrange[index][0], autopct='%1.1f%%', textprops={'fontsize': 7})
            axs[i, j].set_title(titles[index])
    plt.savefig('task2_2_wordpies.png')

    # stacked bar charts
    '''
    dataframe structure:

                monday      friday      sunday

    morning
    afternoon
    evening
    late night

    days come from 'DAY_WEEK_DESC'
    '''
    days = accident[accident['DAY_WEEK_DESC'].isin(['Monday', 'Friday', 'Sunday'])]

    grouped = days.groupby(['DAY_WEEK_DESC', 'TIME_OF_DAY']).size().unstack(fill_value=0)
    grouped.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='Set2')


    #plt.title("Accidents by Time of Day across Days of the Week")
    #plt.xlabel("Day of the Week")
    #plt.ylabel("Number of Accidents")
    #plt.xticks(rotation=45)
    #plt.legend(title="Time of Day", bbox_to_anchor=(1.05, 1), loc='upper left')
    #plt.tight_layout()
    #plt.savefig('task2_2_stackbar.png')

# categorize accident time
def sort_time(time):
    time_format = r'\d{2}:\d{2}'
    if re.search(time_format, time):
        hours = time[:2]
        minutes = time[3:5]
        if (6 <= int(hours) <= 11):
            return "Morning"
        elif (12 <= int(hours) <= 17):
            return "Afternoon"
        elif (18 <= int(hours) <= 23):
            return "Evening"
        else:
            return "Late Night"

task2_2()








