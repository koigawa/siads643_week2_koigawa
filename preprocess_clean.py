"""
This module contains all the clean/preprocessing related functions
Most of these functions are very specialized, and hence cannot be transferred to another dataset.
"""

import pandas as pd

TOTAL_PARTICIPATING_COUNTRIES = 32


def get_result(row, side) -> int:
    """
    This is function used by lambda so that results can be calculated based on away/home match
    and countries can have 3 for a win, 1 for a draw and 0 for a loss.
        Parameters:
            row (Series): A row for the dataframe
            side (String): A string to indicate whether it's calculation for away or home match
        Returns:
            (Intger) A score to indicate a win, draw or a loss
    """
    if side == "home":
        if row.home_score > row.away_score:
            return 3
        if row.home_score < row.away_score:
            return 0
        return 1
    if row.home_score < row.away_score:
        return 3
    if row.home_score > row.away_score:
        return 0
    return 1


def get_goal_diff(row, side) -> int:
    """
    Calculates the difference in score based on home or away games.
        Parameters:
            row (Series): A row for the dataframe
            side (String): A string to indicate whether it's calculation for away or home match
        Returns:
            (Intger) A goal difference, depending on whether home or away games
    """
    if side == "home":
        return row.home_score - row.away_score
    return row.away_score - row.home_score


def return_world_cup_result(
        data,
        country_name,
        tournament_name) -> pd.DataFrame:
    """
    Returns World Cup results for each iteration of the event
        Parameters:
            data (DataFrame): DataFrame for all the results, from the original kaggle dataset
            country_name (String): A string to indicate the hosting nation for
            the World Cup e.g. Qatar 2022
            tournament_name (String): A string to indicate a tournament e.g., FIFA World Cup
        Returns:
            (DataFrame) A dataframe that contains performance of each country, for that tournament
    """

    df = data.copy()
    df = df[((df.tournament == tournament_name) &
             (df.country == country_name))].copy()

    df["home_result"] = df.apply(lambda x: get_result(x, "home"), axis=1)
    df["away_result"] = df.apply(lambda x: get_result(x, "away"), axis=1)
    df["home_goal_diff"] = df.apply(lambda x: get_goal_diff(x, "home"), axis=1)
    df["away_goal_diff"] = df.apply(lambda x: get_goal_diff(x, "away"), axis=1)

    home = df[
        ["tournament", "country", "home_team", "home_result", "home_goal_diff"]
    ].copy()

    away = df[
        ["tournament", "country", "away_team", "away_result", "away_goal_diff"]
    ].copy()

    home.rename(
        columns={
            "home_team": "team",
            "home_result": "result",
            "home_goal_diff": "goal_diff",
        },
        inplace=True,
    )
    away.rename(
        columns={
            "away_team": "team",
            "away_result": "result",
            "away_goal_diff": "goal_diff",
        },
        inplace=True,
    )

    combined = pd.concat([home, away]).copy()

    # Match count is the best indicator of how well the team did
    combined["match_count"] = 1

    # This ordering is not the most accurate, but is systematic way to
    # calculate power rating
    combined = (
        combined.groupby(
            [
                "tournament",
                "country",
                "team"],
            as_index=False) .sum() .sort_values(
            by=[
                "match_count",
                "result",
                "goal_diff"],
            ascending=False) .reset_index(
            drop=True) .reset_index() .rename(
            columns={
                "index": "rank"}))
    combined["wc_result_score"] = (TOTAL_PARTICIPATING_COUNTRIES - (combined["rank"] + 1)) / \
        TOTAL_PARTICIPATING_COUNTRIES + 1 / TOTAL_PARTICIPATING_COUNTRIES

    return combined[["country", "team", "wc_result_score"]]


def combine_two_tournament_results(
        first_tournament_df,
        second_tournament_df) -> pd.DataFrame:
    """
    This function can be used to join results from two tournaments,
    and filter by only relevant columns.
        Parameters:
            first_tournament_df (DataFrame): A dataframe for the result of the first tournament
            second_tournament_df (DataFrame): A dataframe for the result of the second tournament
        Returns:
            cominbed_df (DataFrame) A dataframe that combines the result of the two tournament
    """

    cominbed_df = first_tournament_df.merge(
        second_tournament_df, how="outer", on=["team"]).copy()

    cominbed_df = cominbed_df[
        ["team", "wc_result_score_x", "wc_result_score_y"]
    ]

    cominbed_df = cominbed_df.fillna(0)

    cominbed_df = cominbed_df.melt(id_vars=["team"])

    cominbed_df = cominbed_df.drop(columns=["variable"]).rename(
        columns={"value": "power_rating"}
    )

    cominbed_df = cominbed_df.groupby(["team"], as_index=False).mean()

    cominbed_df = cominbed_df.rename(columns={"team": "country_name"})

    return cominbed_df


def label_previous_champions(
        df,
        first_champion,
        second_champion) -> pd.DataFrame:
    """
    This function is used to label champions of previous World Cup
        Parameters:
            df (DataFrame) A dataframe that combines the result of the two tournament
            first_champion (String): The winner of the first tournament
            second_champion (String): The winner of the second tournament
        Returns:
            df (DataFrame) A dataframe that combines the result of the
            two tournament plus champions labelled
    """
    df["is_former_champion"] = df.apply(
        lambda x: "Y"
        if x["country_name"] == first_champion or x["country_name"] == second_champion
        else "N",
        axis=1,
    )

    return df
