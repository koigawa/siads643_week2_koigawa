"""This is the main module from which the script can be run.
The purpose of this module to read csv data taken from kaggle, and then output
a visualization that shows ranking of countries based on performances in previous
men's FIFA World Cup tournament. Please note that the cleaning process is specific
to the file, so some functions won't run if correct values are not provided
"""
from load import load_csv_data, get_tournament_data
from clean import return_world_cup_result

FILE_URL = "results.csv"
TOURNAMENT_NAME = "FIFA World Cup"
COUNTRY_ONE = 'Qatar'
COUNTRY_TWO = 'Russia'

if __name__ == "__main__":
    print('hello world')

    df = load_csv_data(FILE_URL)
    df = get_tournament_data(TOURNAMENT_NAME, df)

    first_tournament = return_world_cup_result(df, "Qatar",TOURNAMENT_NAME)

    print(first_tournament.head(5))
