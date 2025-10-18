from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from app import USERS


def standardize_data(df):
    scaler = StandardScaler()
    standardized_data = scaler.fit_transform(df)
    standardized_df = pd.DataFrame(standardized_data, columns=df.columns)
    return standardized_df

def store_slider_responses(users):
    responses = []
    for user in users.values():
        responses.append(user["slider_responses"])
    df = pd.DataFrame(responses)
    return df

def model(k):
    users = USERS

    preferences = store_slider_responses(users)
    preferences = standardize_data(preferences)
    knn = NearestNeighbors(n_neighbors=3, metric='euclidean')
    knn.fit(preferences)

