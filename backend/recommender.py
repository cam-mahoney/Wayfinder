from sklearn.preprocessing import StandardScaler
import pandas as pd


def standardize_data(df):
    scaler = StandardScaler()
    standardized_data = scaler.fit_transform(df)
    standardized_df = pd.DataFrame(standardized_data, columns=df.columns)
    return standardized_df

