##############################################
# Scraping old results
##############################################
import re

# Relevant paths

data_root_path = '/home/darren/data/superbru/'

# Example dataframe
# {{'Round':1, 'Home Team':'Celtic', 'Away Team': }, {...}, {...}}

line_array_raw = []

with open(data_root_path + 'darren_picks.txt', 'r') as file:
    for line in file:
        line_array_raw.extend(line.strip().split('\t'))

removal_list = ['Pick', 'Points', '']
line_array = [part for part in line_array_raw if part not in removal_list]


line_iter = iter(line_array)
# print(line_array)

# Extract Scores for games per round
match_columns = ['Round', 'Home team', 'Away Team', 'Home score', 'Away score', 'Home prediction', 'Away prediction', 'Player score']
round_columns = ['Round', 'Slam point', 'Round points']

#for part in line_array:
#    if re.search('Round [0-9]+', part[0]):
#        print(next(line_array))

matches_list = []
rounds_list = []

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
                    round_dict = dict(zip(round_columns,[round_num, slam_pt, round_tot]))
                    rounds_list.append(round_dict)
                    part = next(line_iter)
                    break

                home_team = part
                part = next(line_iter)
                try:
                    home_score = int(part)
                    away_score = int(next(line_iter))
                    away_team = next(line_iter)
                except ValueError:
                    home_score = -1
                    away_score = -1
                    away_team = part

                home_pred = next(line_iter)
                if home_pred == 'No pick':
                    away_pred = 'No pick'
                    player_score = '0'
                else:
                    away_pred = next(line_iter)
                    player_score = next(line_iter)

                obs = [round_num, home_team, away_team, home_score, away_score, home_pred, away_pred, player_score]
                match_dict = dict(zip(match_columns,obs))
                matches_list.append(match_dict)
                print(match_dict)
                part = next(line_iter)


    except StopIteration:
        print("End of iterator.")
        break

print(matches_list)