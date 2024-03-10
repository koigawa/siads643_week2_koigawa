""" This module contains all the load related functions """

import pandas as pd

def load_csv_data(file_path) -> pd.DataFrame:
    """
    This function creates a dataframe from a csv file specified by file_path.
        Parameter:
            file_path (String): Indicates the path of the input file
        Returns:
            (DataFrame): A dataframe created after reading the CSV
    """
    return pd.read_csv(file_path)

def get_tournament_data(tournament_name, df) -> pd.DataFrame:
    """
    This function extracts information pertaining to a specific tournament.
        Parameter:
            tournament_name (String): A string to indicate name of the tournament for extraction
            df (DataFrame): A dataframe that contains results from all football events
        Returns:
            (DataFrame): A dataframe with only relevant tournament data
    """
    return df[df.tournament == tournament_name].copy()


