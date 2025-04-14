import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans


def task3_2():
    # Data Preparation
    file_path = "/course/filtered_vehicle.csv"
    filtered_vehicles_df = pd.read_csv(file_path)
    cols = ["VEHICLE_YEAR_MANUF", "VEHICLE_BODY_STYLE", "VEHICLE_MAKE", 'NO_OF_WHEELS', 'NO_OF_CYLINDERS', 'SEATING_CAPACITY', 'TARE_WEIGHT', 'TOTAL_NO_OCCUPANTS']
    filtered_vehicles_df = filtered_vehicles_df[cols]
    grouped_df = filtered_vehicles_df.groupby(["VEHICLE_YEAR_MANUF", "VEHICLE_BODY_STYLE", "VEHICLE_MAKE"]).mean().reset_index()

    # Normalisation
    norm_cols = ['NO_OF_WHEELS', 'NO_OF_CYLINDERS', 'SEATING_CAPACITY', 'TARE_WEIGHT', 'TOTAL_NO_OCCUPANTS']
    normalised_df = MinMaxScaler().fit_transform(grouped_df[norm_cols])

    # The Elbow Method
    k_ranges = range(1, 11) # for k from 1 to 10
    sse = []
    rand_state = 20008
    for k in k_ranges:
        kmeans = KMeans(n_clusters=k, random_state=rand_state)
        kmeans.fit(normalised_df)
        sse.append(kmeans.inertia_)
    
    # Line plot
    plt.plot(k_ranges, sse)
    plt.xticks(np.arange(11))
    plt.xlabel('Number of clusters')
    plt.ylabel('Sum of Squared Error')
    plt.title('The Elbow Method')

    plt.savefig('task3_2_elbow.png')

    return
