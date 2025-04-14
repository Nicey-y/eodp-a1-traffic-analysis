import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
import regex as re

from task1_1 import task1_1

def task1_2():

    #Getting the updated dataframe from Task 1.1
    rdata = task1_1()

    #Task 1.2.1

    #Ref: https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py

    #Pulling out data from dataframe
    age_category = ("Under 16", "17-25", "26-39", "40-64", "65+", "Unknown")
    accidents = {
        'Seatbelt Worn':  rdata[rdata['HELMET_BELT_WORN'] == 1].groupby('AGE_CATEGORY').size().reindex(age_category, fill_value=0).values,
        'Seatbelt Not Worn': rdata[rdata['HELMET_BELT_WORN'] == 8].groupby('AGE_CATEGORY').size().reindex(age_category, fill_value=0).values,
    }

    #Creating the plot
    x = np.arange(len(age_category))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(figsize=(15, 10))
    colors = ['#4CAF50', '#FF5722']


    for i, (attribute, measurement) in enumerate(accidents.items()):
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute,color=colors[i])
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Axes titles
    ax.set_xlabel('Age Group', fontsize=18)
    ax.set_ylabel('Number of Accidents', fontsize=18)

    # Adjusting axes ticks
    ax.set_xticks(x + width / 2)  # Adjust tick positions to center them
    ax.set_xticklabels(age_category, fontsize=16)
    plt.yticks(fontsize=13)  # Increase font size of y-ticks

    ax.set_title('Seatbelt Use Across Different Age Groups',fontsize=20)
    ax.legend(fontsize=15)

    # Save the plot as a PNG file
    plt.savefig('task1_2_age.png', format='png') 

    
    #Task 1.2.2

    # Pie Chart Reference: https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html#sphx-glr-gallery-pie-and-polar-charts-pie-features-py

    # Computing relevant numbers for pie chart
    drivers_seatbelt = len(rdata[(rdata['HELMET_BELT_WORN'] == 1) & (rdata['ROAD_USER_TYPE'].isin([2, 7]))])
    drivers_noseatbelt = len(rdata[(rdata['HELMET_BELT_WORN'] == 8) & (rdata['ROAD_USER_TYPE'].isin([2, 7]))])
    passenger_seatbelt = len(rdata[(rdata['HELMET_BELT_WORN'] == 1) & (rdata['ROAD_USER_TYPE'].isin([3, 8]))])
    passenger_noseatbelt = len(rdata[(rdata['HELMET_BELT_WORN'] == 8) & (rdata['ROAD_USER_TYPE'].isin([3, 8]))])

    labels = ['Seatbelt', 'No Seatbelt']
    driversdata = [drivers_seatbelt, drivers_noseatbelt]
    passengersdata = [passenger_seatbelt, passenger_noseatbelt]

    fig, axs = plt.subplots(1, 2, figsize=(15, 10))
    fig.suptitle('Seatbelt Usage by Driver and Passenger', fontsize=26)
    colors = ['#3CB371', '#B22222']


    # First pie: Drivers
    axs[0].pie(driversdata, labels=labels, autopct='%1.0f%%',textprops={'fontsize': 18},colors=colors)
    axs[0].set_title('Drivers',fontsize=20)

    # Second pie: Passengers
    axs[1].pie(passengersdata, labels=labels, autopct='%1.0f%%',textprops={'fontsize': 18},colors=colors)
    axs[1].set_title('Passengers',fontsize=20)

    plt.tight_layout()
    fig.legend(labels, ncol=2, fontsize=18,bbox_to_anchor=(0.7, 0.9))
    plt.subplots_adjust(wspace=0.6)
    
    plt.savefig('task1_2_driver.png', format='png')

    # Task 1.2.3

    #Created based on discussion forum (#72) deciding which abbreviations classify as Front and Rear Passenger

    #The following function takes a "SEATING_POSITION" and assigns it as front passenger, rear passenger or other
    def assign_pos(pos):
        pos = str(pos)
        if "R" in pos:
            return "Rear Passenger"
        elif re.search(r'(LF|CF|PL)',pos):
            return "Front Passenger"
        else: return "Other"
        
    #Collecting data needed for pie chart
    rear_seatbelt = rdata[(rdata['HELMET_BELT_WORN'] == 1) & (rdata['SEATING_POSITION'].apply(assign_pos) == "Rear Passenger")].shape[0]
    rear_noseatbelt = rdata[(rdata['HELMET_BELT_WORN'] == 8) & (rdata['SEATING_POSITION'].apply(assign_pos) == "Rear Passenger")].shape[0]
    front_seatbelt = rdata[(rdata['HELMET_BELT_WORN'] == 1) & (rdata['SEATING_POSITION'].apply(assign_pos) == "Front Passenger")].shape[0]
    front_noseatbelt = rdata[(rdata['HELMET_BELT_WORN'] == 8) & (rdata['SEATING_POSITION'].apply(assign_pos) == "Front Passenger")].shape[0]
                            
    labels = ['Seatbelt', 'No Seatbelt']
    frontseat = [front_seatbelt, front_noseatbelt]
    rearseat = [rear_seatbelt, rear_noseatbelt]

    fig, axs = plt.subplots(1, 2, figsize=(15, 10))
    fig.suptitle('Seatbelt Usage by Seat Position', fontsize=26)
    colors = ['#3CB371', '#B22222']


    # First pie: Frontseat
    axs[0].pie(frontseat, labels=labels, autopct='%1.0f%%',textprops={'fontsize': 18},colors=colors)
    axs[0].set_title('Frontseat Passenger',fontsize=20)

    # Second pie: Rearseat
    axs[1].pie(rearseat, labels=labels, autopct='%1.0f%%',textprops={'fontsize': 18},colors=colors)
    axs[1].set_title('Rearseat Passenger',fontsize=20)

    plt.tight_layout()
    fig.legend(labels, loc='upper center', ncol=2, fontsize=18,bbox_to_anchor=(0.7, 0.9))
    plt.subplots_adjust(wspace=0.6)

    plt.savefig('task1_2_seat.png', format='png')
