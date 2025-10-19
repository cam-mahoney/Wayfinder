from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.neighbors import NearestNeighbors
# from app import USERS
import json

USERS = {
    "user_id": {
        "first_name": str,
        "last_name": str,
        "slider_responses": {
            "time_commitment_value": 5,
            "cost_preference": 5,
            "goal_balance": 3,
            "event_frequency": 1,
            "academic": 7,
            "sport_type": 4,
            "competition": 3,
            "leadership": 9,
            "environment_value": 3,
            "social_vs_professional": 6
        }
    },
    "user_ird": {
        "first_name": str,
        "last_name": str,
        "slider_responses": {
            "time_commitment_value": 5,
            "cost_preference": 5,
            "goal_balance": 3,
            "event_frequency": 1,
            "academic": 7,
            "sport_type": 4,
            "competition": 3,
            "leadership": 9,
            "environment_value": 3,
            "social_vs_professional": 6
        }
    }
    
}


def standardize_data(clubs, preferences):
    scaler = StandardScaler()
    scaler.fit(clubs)
    standardized_clubs = scaler.transform(clubs)
    standardized_preferences = scaler.transform(preferences)
    standardized_preferences = pd.DataFrame(standardized_preferences, columns=preferences.columns)
    standardized_clubs = pd.DataFrame(standardized_clubs, columns=clubs.columns)
    return standardized_clubs, standardized_preferences

def store_slider_responses(users,user):
    responses = []
    for u in users.keys():
        if user == u:
            responses.append(users[u]["slider_responses"])
    df = pd.DataFrame(responses)
    return df

def extract_club_features(clubs):
    df = pd.DataFrame(clubs)
    numerical_columns = ["time_commitment_value", "cost_preference", "goal_balance", 
                     "event_frequency", "academic", "sport_type", "competition", 
                     "leadership", "environment_value", "social_vs_professional"]
    df = df[numerical_columns]
    return df

def model(user, k):
    users = USERS
    with open(r'backend\data\orgs.json', 'r') as file:
        clubs_dict = json.load(file)
    clubs_df = extract_club_features(clubs_dict)
    preferences = store_slider_responses(users, user)
    clubs_df,preferences = standardize_data(clubs_df,preferences)
    knn = NearestNeighbors(n_neighbors=k, metric='euclidean')
    knn.fit(clubs_df)
    distances, indices = knn.kneighbors(preferences)
    nearest_clubs = []

    for idx in indices[0]:
        nearest_clubs.append(clubs_dict[idx]['id'])

    return nearest_clubs

print(model("user_id",3))