import pandas as pd
import re
import matplotlib.pyplot as plt

def task2_2():
    accident_df = pd.read_csv("accident.csv")

    # categorizes accident times acc. to TIME_OF_DAY categories
    accident_df['TIME_OF_DAY'] = accident_df['ACCIDENT_TIME'].apply(lambda x: sort_time(x))

    '''
    Plot 1
    '''

    time_occurrences = {}

    # frequency of each TIME_OF_DAY category occurrence
    for time in accident_df['TIME_OF_DAY']:
        if time not in time_occurrences:
            time_occurrences[time] = 1
        else:
            time_occurrences[time] += 1

    # dataframe with number of accidents per time of day
    time_occurrences_df = pd.DataFrame(list(time_occurrences.items()), columns = ['TIME_OF_DAY', 'ACCIDENT_FREQUENCY'])

    # set and sort TIME_OF_DAY elements as time appears in the day
    time_occurrences_df = time_occurrences_df.set_index('TIME_OF_DAY', drop=False)
    time_occurrences_df = time_occurrences_df.reindex(index=['Morning', 'Afternoon', 'Evening', 'Late Night'])

    plt.clf()
    # plot bar chart
    plt.figure()
    plt.title("Number of Accidents by Time of Day")
    plt.bar(time_occurrences_df['TIME_OF_DAY'], time_occurrences_df['ACCIDENT_FREQUENCY'])
    plt.xlabel("Time of Day")
    plt.ylabel("Number of Accidents")
    plt.xticks(rotation=30)
    plt.tight_layout(pad=2.0)
    plt.savefig('task2_2_timeofday.png')

    ###################################################################################################################

    plt.clf()
    '''
    Plot 2
    '''

    word_counts = {}
    dca_desc_top10_words = []

    for time in time_occurrences_df.index:
        time_filtered = accident_df[accident_df['TIME_OF_DAY'] == time]
        for desc in time_filtered['DCA_DESC']:

            split_desc = re.findall(r'\b\w+\b', desc) # tokenize words

            for word in split_desc:
                if word not in word_counts:
                    word_counts[word] = 1
                else:
                    word_counts[word] += 1
        
        # arrange acc. to most frequently occurring words
        sorted_word_counts = sorted(list(word_counts.items()), key=lambda x: x[1], reverse=True)
        
        # store 10 most frequent words
        dca_desc_top10_words.append(sorted_word_counts[:10])
        word_counts = {}

    '''
    structure of dca_desc_top10_words:

    [[(word1, count1), (word2, count2), ... for 'Morning'], 
    [(word 1, count1), ... for 'Afternoon'], 
    [for 'Evening'], [for 'Late Night']]

    each sub-list corresponds to 1 of 4 pie charts.
    '''

    
    dca_desc_words_rearranged = []
    for top_words in dca_desc_top10_words:
        # for each sub_list containing 10 most frequent words in each TIME_OF_DAY
        rearrange = list(map(list, zip(*top_words)))

        # separates words and frequencies (removes tuple format)
        dca_desc_words_rearranged.append(rearrange)
    
    # plot the pie charts
    titles = ['Morning', 'Afternoon', 'Evening', 'Late Night']
    fig, axs = plt.subplots(2, 2, figsize=(12, 10)) # 2x2 grid
    fig.suptitle('10 Most Frequent Accident Terms by Time Of Day', fontsize=20)

    for i in range(2):
        for j in range(2):
            # for each pie plot
            index = i * 2 + j
            axs[i, j].pie(
                dca_desc_words_rearranged[index][1], 
                labels=dca_desc_words_rearranged[index][0], 
                autopct='%1.1f%%', 
                textprops={'fontsize': 10})
            axs[i, j].set_title(titles[index], fontsize=16)
    plt.savefig('task2_2_wordpies.png')

    ###################################################################################################################
    
    plt.clf()

    '''
    Plot 3

    required dataframe structure:

                monday      friday      sunday

    morning
    afternoon
    evening
    late night

    days come from 'DAY_WEEK_DESC'
    '''

    # days of the week for which data needs to be shown
    select_days = accident_df[accident_df['DAY_WEEK_DESC'].isin(['Monday', 'Friday', 'Sunday'])]

    selected_days_ordered = ['Monday', 'Friday', 'Sunday']

    grouped = select_days.groupby(['DAY_WEEK_DESC', 'TIME_OF_DAY']).size().unstack(fill_value=0)
    grouped = grouped.reindex(selected_days_ordered)
    
    grouped.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='Set2')

    # plot stacked bar chart
    plt.title("Accidents by Time of Day across Days of the Week")
    plt.xlabel("Day of the Week")
    plt.ylabel("Number of Accidents")
    plt.xticks(rotation=45)
    plt.legend(title="Time of Day", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('task2_2_stackbar.png')

    ###################################################################################################################

'''
Function to categorize time with format HH:MM:SS (from 'ACCIDENT_TIME')
'''

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
