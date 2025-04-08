import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

def task3_3():
    # Data Preparation
    #file_path = "/course/filtered_vehicle.csv"
    file_path = "./a1-datasets/filtered_vehicle.csv"
    filtered_vehicles_df = pd.read_csv(file_path)
    cols = ['ACCIDENT_NO', "VEHICLE_YEAR_MANUF", "VEHICLE_BODY_STYLE", "VEHICLE_MAKE", 'VEHICLE_TYPE_DESC', 'NO_OF_WHEELS', 'NO_OF_CYLINDERS', 'SEATING_CAPACITY', 'TARE_WEIGHT', 'TOTAL_NO_OCCUPANTS']
    filtered_vehicles_df = filtered_vehicles_df[cols]
    grouped_df = filtered_vehicles_df.groupby(["VEHICLE_YEAR_MANUF", "VEHICLE_BODY_STYLE", "VEHICLE_MAKE", 'VEHICLE_TYPE_DESC']).agg({'ACCIDENT_NO': 'count', 'NO_OF_WHEELS': 'mean', 'NO_OF_CYLINDERS': 'mean', 'SEATING_CAPACITY': 'mean', 'TARE_WEIGHT': 'mean', 'TOTAL_NO_OCCUPANTS': 'mean'}).reset_index()

    # Normalisation
    norm_cols = ['NO_OF_WHEELS', 'NO_OF_CYLINDERS', 'SEATING_CAPACITY', 'TARE_WEIGHT', 'TOTAL_NO_OCCUPANTS']
    normalised_df = MinMaxScaler().fit_transform(grouped_df.copy()[norm_cols])

    # KMeans with k = 3
    rand_state = 20008
    k = 3
    clusters = KMeans(n_clusters=k, random_state=rand_state)
    clusters.fit(normalised_df)

    # Undersampling
    grouped_df['cluster'] = clusters.labels_

    # Produce .csv files
    grouped_df.set_index('cluster', inplace=True, drop=True)
    for k in range(3): write_to_csv(grouped_df, k)

    return

def write_to_csv(df, cluster_num):
    cluster_df = df.filter(like=str(cluster_num), axis=0)
    cluster_df = cluster_df.sort_values(by='cluster', ascending=False)
    
    filename = '3cluster_task3_3_cluster{k}.csv'.format(k=cluster_num)
    cluster_df.head(100).to_csv(filename, index=False)

task3_3()