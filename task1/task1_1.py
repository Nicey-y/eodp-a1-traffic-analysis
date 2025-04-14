import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt


def task1_1():
    rdata = pd.read_csv(r"/course/person.csv")
    #print(rdata.shape)

    #Task 1.1.1 starts here

    #Count the frequency of each "value"

    helmbelt = rdata["HELMET_BELT_WORN"]
    values, counts = np.unique(helmbelt, return_counts=True)

    # Find mode and fill NaN values with the mode

    mode_helmetbelt = helmbelt.mode()[0]
    helmbelt = helmbelt.fillna(mode_helmetbelt)
    rdata["HELMET_BELT_WORN"] = helmbelt

    #Reprint the frequency of all values (sanity check)
    #values, counts = np.unique(helmbelt, return_counts=True)
    #for value, count in zip(values, counts):
        #print(r"Helmet/Belt Value:", value, ", Count:", count)

    # Task 1.1.2 starts here

    # One-Hot-Encoding the Sex Column

    #Coverting empty values with "Unknown"
    sex = rdata["SEX"]                     
    sex = sex.fillna("U")                 
    rdata["SEX"] = sex                    

    sex_column = rdata["SEX"].values.reshape(-1, 1)
    onehot_encoder1 = OneHotEncoder(sparse_output=False)
    encoded_data1 = onehot_encoder1.fit_transform(sex_column)
    #print(encoded_data1)
    #print(onehot_encoder1.categories_)

    #Create new columns for SEX_M, SEX_F, SEX_U
    rdata[['SEX_Female', 'SEX_Male', 'SEX_Unknown']] = encoded_data1
    #print(rdata)


    # One-Hot-Encoding the ROAD_USER_TYPE_DESC Column

    user_column = rdata["ROAD_USER_TYPE_DESC"].values.reshape(-1, 1)
    onehot_encoder2 = OneHotEncoder(sparse_output=False)
    encoded_data2 = onehot_encoder2.fit_transform(user_column)
    #print(encoded_data2)
    #print(onehot_encoder2.categories_)

    #Create new columns
    rdata[['ROAD_USER_DESC_Bicyclists', 'ROAD_USER_DESC_Drivers','ROAD_USER_DESC_E-scooter_Rider','ROAD_USER_DESC_Motorcyclists',
        'ROAD_USER_DESC_Not_Known','ROAD_USER_DESC_Passengers','ROAD_USER_DESC_Pedestrians','ROAD_USER_DESC_Pillion_Passengers']] = encoded_data2
    #print(rdata)

    # Task 1.1.3

    # Verifing all given inputs for age category

    #age = rdata["AGE_GROUP"]
    #values, counts = np.unique(age, return_counts=True)
    #for value, count in zip(values, counts):
        #print(r"Age Group:", value, ", Count:", count)

    #Simple if block to determine the age category of a given age group

    def converter(age_group):
        if age_group == "0-4" or age_group == "5-12" or age_group == "13-15":
            return "Under 16"
        elif age_group == "16-17" or age_group == "18-21" or age_group == "22-25":
            return "17-25"
        elif age_group == "26-29" or age_group == "30-39":
            return "26-39"
        elif age_group == "40-49" or age_group == "50-59" or age_group == "60-64":
            return "40-64"
        elif age_group == "65-69" or age_group == "70+":
            return "65+"
        else: return "Unknown"

    rdata["AGE_CATEGORY"] = rdata["AGE_GROUP"].apply(lambda x: converter(x))
    #print(rdata)

    return(rdata)
