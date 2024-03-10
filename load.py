""" This module contains all the load related functions """

import pandas as pd

def load_csv_data(file_path) -> pd.DataFrame:
    return pd.read_csv(file_path)

def get_tournament_data(tournament_name, df) -> pd.DataFrame:
    return df[df.tournament == tournament_name].copy()


