import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import specific_data as sd

# Import data
match_col_dtypes = {'Round': 'int',
                    'Home team': 'category',
                    'Away team': 'category',
                    'Home goals': 'int',
                    'Away goals': 'int',
                    'Home prediction': 'int',
                    'Away prediction': 'int',
                    'Player score': 'category'}

round_col_dtypes = {'Round': 'int',
                    'Slam point': 'int',
                    'Round points': 'float'}

df_collection = {}
df_round_collection = {}
for person in sd.players:
    df_person = pd.read_csv(sd.csv_save_path + person + '_scores.csv', dtype=match_col_dtypes)
    df_round = pd.read_csv(sd.csv_save_path + person + '_rounds.csv', dtype=round_col_dtypes)
    df_collection[person] = df_person
    df_round_collection[person] = df_round


match_cols = ['Round', 'Home team', 'Away team', 'Home goals', 'Away goals']
df_match_results = df_collection[sd.players[0]][match_cols]

df_predictions = df_match_results
for person, df in df_collection.items():
    df_predictions = df_predictions.merge(df, on=match_cols, suffixes=(None, '_'+person), validate='one_to_one')

points_map = {'0NoPick': 0.0, '0WRONG': 0.0, '1.5CLOSE': 1.5, '1RESULT': 1.0, '3EXACT': 3.0, 'Postponed': 0.0}

# Since 'suffixes' does not force a suffix on the first instance, I treat the first player separately

df_predictions[sd.players[0].capitalize() + ' points'] = df_predictions['Player score'].replace(points_map).astype(float)
for person in sd.players[1:]:
    df_predictions[person.capitalize() + ' points'] = df_predictions['Player score_'+person].replace(points_map).astype(float)

points_per_round = df_predictions.groupby('Round')[[ps.capitalize() + ' points' for ps in sd.players]].sum()

#for person in sd.players:
#    sns.lineplot(data=points_per_round, x='Round', y=person.capitalize() +' points')

#plt.title('Points per round')
#plt.xlabel('Round')
#plt.ylabel('Points')
#plt.legend(sd.players)
#plt.show()