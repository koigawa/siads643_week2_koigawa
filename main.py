"""This is the main module from which the script can be run.
The purpose of this module to read csv data taken from kaggle, and then output
a visualization that shows ranking of countries based on performances in previous
men's FIFA World Cup tournament. Please note that the cleaning process is specific
to the file, so some functions won't run if correct values are not provided
"""
from load import load_csv_data, get_tournament_data
from preprocess_clean import (
    return_world_cup_result,
    combine_two_tournament_results,
    label_previous_champions)
from visualize import get_ranking_chart

# Fixed constants for the content
TOURNAMENT_NAME = "FIFA World Cup"
COUNTRY_ONE = 'Qatar'
COUNTRY_TWO = 'Russia'
FIRST_CHAMPION = 'France'
SECOND_CHAMPION = 'Argentina'

# Fixed constants for visualization
TITLE = "FIFA World Cup Power Ratings"
SUBTITLE = "Russia 2018, Qatar 2022"
METRIC_NAME = "power_rating"
SCALE = [0, 1.2]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_file",
        help="File path for dataset downloaded from Kaggle (CSV)")
    parser.add_argument(
        "output_file",
        help="File path for the output visualization (PNG)")
    args = parser.parse_args()

    df = load_csv_data(args.input_file)
    df = get_tournament_data(TOURNAMENT_NAME, df)

    first_tournament = return_world_cup_result(
        df, COUNTRY_ONE, TOURNAMENT_NAME)
    second_tournament = return_world_cup_result(
        df, COUNTRY_TWO, TOURNAMENT_NAME)

    combined_df = combine_two_tournament_results(
        first_tournament, second_tournament)

    combined_df = label_previous_champions(
        combined_df, FIRST_CHAMPION, SECOND_CHAMPION)

    get_ranking_chart(
        TITLE,
        SUBTITLE,
        combined_df,
        METRIC_NAME,
        SCALE).save(
        args.output_file)
