import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

file_path0 = 'task3_3_cluster0_test.csv'
file_path1 = 'task3_3_cluster1_test.csv'
file_path2 = 'task3_3_cluster2_test.csv'

cluster0 = pd.read_csv(file_path0)
cluster1 = pd.read_csv(file_path1)
cluster2 = pd.read_csv(file_path2)

# Scatter plot
fig, axs = plt.subplots(2, 2)
x0 = cluster0['VEHICLE_YEAR_MANUF']
y0 = cluster0['ACCIDENT_NO']
axs[0, 0].scatter(x0, y0, alpha=0.4, c='red')

x1 = cluster1['VEHICLE_YEAR_MANUF']
y1 = cluster1['ACCIDENT_NO']
axs[0, 1].scatter(x1, y1, alpha=0.4, c='green')

x2 = cluster2['VEHICLE_YEAR_MANUF']
y2 = cluster2['ACCIDENT_NO']
axs[1, 0].scatter(x2, y2, alpha=0.4, c='blue')

for ax in axs.flat:
    ax.set(xlabel='Year Manufactured', ylabel='Number of crashes')

#plt.legend()
#plt.savefig('3_separate_clusters.png')

