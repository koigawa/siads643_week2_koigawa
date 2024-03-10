import pandas as pd

TOTAL_PARTICIPATING_COUNTRIES = 32

def get_result(row, side) -> int:
    if side == "home":
        if row.home_score > row.away_score:
            return 3
        elif row.home_score < row.away_score:
            return 0
        else:
            return 1
    else:
        if row.home_score < row.away_score:
            return 3
        elif row.home_score > row.away_score:
            return 0
        else:
            return 1


# This function returns the goal difference for both home and away
def get_goal_diff(row, side) -> int:
    if side == "home":
        return row.home_score - row.away_score
    else:
        return row.away_score - row.home_score


# Returns World Cup results for each iteration of the event
def return_world_cup_result(data, country_name, tournament_name):

    df = data.copy()
    df = df[((df.tournament == "FIFA World Cup") & (df.country == country_name))].copy()

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

    # This ordering is not the most accurate, but is systematic way to calculate power rating
    combined = (
        combined.groupby(["tournament", "country", "team"], as_index=False)
        .sum()
        .sort_values(by=["match_count", "result", "goal_diff"], ascending=False)
        .reset_index(drop=True)
        .reset_index()
        .rename(columns={"index": "rank"})
    )
    combined["wc_result_score"] = (TOTAL_PARTICIPATING_COUNTRIES - (combined["rank"] + 1)) / TOTAL_PARTICIPATING_COUNTRIES + 1 / TOTAL_PARTICIPATING_COUNTRIES

    return combined[["country", "team", "wc_result_score"]]