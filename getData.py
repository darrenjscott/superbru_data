##############################################
# Scraping old results
##############################################
import re
from useful_fns import dict_to_csv
import specific_data as sd

# Keys for two dictionaries we will save
match_columns = ['Round', 'Home team', 'Away team', 'Home goals', 'Away goals', 'Home prediction', 'Away prediction', 'Player score']
round_columns = ['Round', 'Slam point', 'Round points']


for player in sd.players:
    who_picks = player + '_picks.txt'
    line_array_raw = []

    with open(sd.data_root_path + who_picks, 'r') as file:
        for line in file:
            line_array_raw.extend(line.strip().split('\t'))

    # This raw data contains some strings it is just easier to remove
    removal_list = ['Pick', 'Points', '']
    line_array = [part for part in line_array_raw if part not in removal_list]

    # Make iterable to extract what we need as we go through until we get to the end
    line_iter = iter(line_array)

    # Holds list of dictionaries.
    # matches_list - one dictionary for each match
    # rounds_list - one dictionary with slam points (+other) for each round
    matches_list = []
    rounds_list = []

    # Iterate through the old file and populate the matches_list and rounds_list with dictionaries
    # Structure of the following relies a lot on knowing how the text-file were obtained
    while True:
        try:
            part = next(line_iter)
            if re.search('Round [0-9]+', part):
                rn_st, rn_fin = re.search('[0-9]+', part).span()
                round_num = int(part[rn_st:rn_fin])

                part = next(line_iter)
                while not re.search('Round [0-9]+', part):
                    if part == 'Slam Point':
                        slam_pt = int(next(line_iter))
                        next(line_iter)
                        round_tot = float(next(line_iter))
                        round_dict = dict(zip(round_columns, [round_num, slam_pt, round_tot]))
                        rounds_list.append(round_dict)
                        break

                    home_team = part
                    part = next(line_iter)
                    try:
                        home_goals = int(part)
                        away_goals = int(next(line_iter))
                        away_team = next(line_iter)
                        game_played = True
                    except ValueError:
                        # If a game is postponed, the next value is the away team and not the home score
                        # so a ValueError is raised in the code preceding when int() is tried.
                        # For now save postponed games as -1,-1
                        home_goals = -1
                        away_goals = -1
                        away_team = part
                        game_played = False

                    part = next(line_iter)
                    # 'No pick' only shows for postponed matches
                    # (def) is contained in a string for
                    # default picks (which we disabled)
                    if part == 'No pick':
                        home_prediction = -1
                        away_prediction = -1
                        player_score = '0NoPick'
                    elif '(def)' in part:
                        home_prediction = -1
                        away_prediction = -1
                        player_score = '0NoPick'
                        next(line_iter)
                    else:
                        home_prediction = int(part)
                        away_prediction = int(next(line_iter))
                        if game_played:
                            player_score = next(line_iter)
                        else:
                            player_score = 'Postponed'

                    obs = [round_num, home_team, away_team, home_goals, away_goals, home_prediction, away_prediction, player_score]
                    match_dict = dict(zip(match_columns, obs))
                    matches_list.append(match_dict)
                    part = next(line_iter)

        except StopIteration:
            print("End of iterator.")
            break

    dict_to_csv(sd.csv_save_path + player + '_scores.csv', matches_list)
    dict_to_csv(sd.csv_save_path + player + '_rounds.csv', rounds_list)
