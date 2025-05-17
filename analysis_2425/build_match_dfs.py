import pandas as pd


def build_match_dfs(match_dict):

    # Construct empty DF to hold list of all goals
    goals_df_columns = ["match_id", "date", "ko_time", "home_team",
                        "away_team", "player_id", "first_name", "last_name",
                        "player_side", "minute", "og"]
    
    match_df_columns = ["match_id", "date", "ko_time", "home_team",
                        "away_team", "referee", "attendance"]
    goals_df = pd.DataFrame(columns=goals_df_columns)
    matches_df = pd.DataFrame(columns=match_df_columns)

    for idx, (match_id, match_raw) in enumerate(match_dict.items()):
        # There is one level to go through
        match = match_raw["match"]

        #id = match["id"]
        date = match["date"]
        ko_time = match["time"]
        home_team = match["home-team"]["name"]
        away_team = match["away-team"]["name"]
        referee = match["referee"]
        attendance = match["attendance"]

        if "goals" in match["home-team"].keys():
            for goal in match["home-team"]["goals"]:
                first_name = goal["player"]["first-name"]
                last_name = goal["player"]["last-name"]
                player_id = goal["player"]["id"]
                minute = goal["minute"]
                player_side = "home"
                if "own-goal" in goal.keys():
                    og = goal["own-goal"]
                else:
                    og = False
                
                data_row = [[match_id, date, ko_time, home_team, away_team,
                            player_id, first_name, last_name, player_side,
                            minute, og]]
                new_entry = pd.DataFrame(data_row,
                                         columns=goals_df_columns)
                goals_df = pd.concat([goals_df, new_entry], ignore_index=True)

        match_data = [[match_id, date, ko_time, home_team, away_team,
                        referee, attendance]]
        match_entry = pd.DataFrame(match_data,
                                   columns=match_df_columns)
        matches_df = pd.concat([matches_df, match_entry], ignore_index=True)

    # Consider swaping out match_id with date and ko_time
    goals_df.sort_values(["match_id", "minute"], inplace=True)
    return matches_df, goals_df


def build_match_table(match_dict):
    # Construct empty DF to hold list of all goals
    match_df_columns = ["match_id", "date", "ko_time", "home_team", "away_team",
                        "referee", "attendance"]
    match_df = pd.DataFrame(columns=match_df_columns)

    for idx, (match_id, match_raw) in enumerate(match_dict.items()):
        # There is one level to go through
        match = match_raw["match"]

        #id = match["id"]
        date = match["date"]
        ko_time = match["time"]
        home_team = match["home-team"]["name"]
        away_team = match["away-team"]["name"]
        referee = match[""]
        
        goals_df = pd.concat([goals_df, new_entry], ignore_index=True)

    # Consider swaping out match_id with date and ko_time
    goals_df.sort_values(["match_id", "minute"], inplace=True)
    return goals_df
