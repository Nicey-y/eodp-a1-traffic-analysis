import pandas as pd
import matplotlib.pyplot as plt

def task3_1():
    # Data Grouping
    file_path = "/course/filtered_vehicle.csv"
    filtered_vehicles_df = pd.read_csv(file_path)
    filtered_vehicles_df = filtered_vehicles_df[["ACCIDENT_NO", "VEHICLE_YEAR_MANUF", "VEHICLE_BODY_STYLE", "VEHICLE_MAKE"]]

    grouped_df = filtered_vehicles_df.groupby(["VEHICLE_YEAR_MANUF", "VEHICLE_BODY_STYLE", "VEHICLE_MAKE"]).count().reset_index()

    # Scatter plot
    x = grouped_df['VEHICLE_YEAR_MANUF']
    y = grouped_df['ACCIDENT_NO']
    plt.scatter(x, y, alpha=0.4, label='Crashes vs (manufacturer-style-year)')

    plt.xlabel('Year Manufactured')
    plt.ylabel('Number of crashes')
    plt.title('Number of crashes for each unique manufacturer-body style-year combination')

    plt.show()
    #plt.savefig('task3_1_scatter.png')

    return

task3_1()