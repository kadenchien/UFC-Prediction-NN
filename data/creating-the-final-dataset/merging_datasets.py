import pandas as pd

list1_df = pd.read_csv('/Users/kevinliu/Desktop/UFC-Prediction-NN/data/creating-the-final-dataset/list1_full.csv')
list2_df = pd.read_csv('/Users/kevinliu/Desktop/UFC-Prediction-NN/data/creating-the-final-dataset/list2_full.csv')
fighters_df = pd.read_csv('/Users/kevinliu/Desktop/UFC-Prediction-NN/data/creating-the-final-dataset/all_fighters_cleaned_database.csv')

# Merge the dataframes based on 'original_order'
merged_df = pd.merge(list1_df, list2_df, on='original_order', suffixes=('_1', '_2'))



# Columns to drop from the merged dataframe
columns_to_drop = [
    'event_2', 'fighter_1_2', 'fighter_2_2', 'fighter_1_result_2', 'fighter_2_result_2',
    'fighter_1_knockdowns_2', 'fighter_2_knockdowns_2', 'fighter_1_ss_2', 'fighter_2_ss_2',
    'fighter_1_ss_pct_2', 'fighter_2_ss_pct_2', 'fighter_1_total_strikes_2', 'fighter_2_total_strikes_2',
    'fighter_1_takedowns_2', 'fighter_2_takedowns_2', 'fighter_1_takedown_pct_2', 'fighter_2_takedown_pct_2',
    'fighter_1_submission_attempts_2', 'fighter_2_submission_attempts_2', 'fighter_1_reverses_2',
    'fighter_2_reverses_2', 'fighter_1_control_2', 'fighter_2_control_2', 'fighter_1_head_ss_2',
    'fighter_2_head_ss_2', 'fighter_1_body_ss_2', 'fighter_2_body_ss_2', 'fighter_1_leg_ss_2',
    'fighter_2_leg_ss_2', 'fighter_1_distance_ss_2', 'fighter_2_distance_ss_2', 'fighter_1_clinch_ss_2',
    'fighter_2_clinch_ss_2', 'fighter_1_ground_ss_2', 'fighter_2_ground_ss_2'
]

# Drop specified columns
merged_df.drop(columns=columns_to_drop, inplace=True)

#NOW I WANT TO ADD THE HEIGHT AND STUFF FROM THE ALL_FIGHTERS_CLEANED_DATABASE

columns_needed = [
    'Name', 'Wins', 'Losses', 'Draws', 'Style_Boxing', 'Style_Brawler', 'Style_Brazilian Jiu-Jitsu',
    'Style_Freestyle', 'Style_Grappler', 'Style_Jiu-Jitsu', 'Style_Judo', 'Style_Karate', 'Style_Kickboxer',
    'Style_Kung Fu', 'Style_Kung-Fu', 'Style_MMA', 'Style_Muay Thai', 'Style_Sambo', 'Style_Striker',
    'Style_Wrestler', 'Style_Wrestling', 'Style_Taekwondo', 'Age', 'Height', 'Reach'
]
fighters_df = fighters_df[columns_needed]


# Merge additional attributes for fighter_1_1
merged_with_fighter1 = pd.merge(merged_df, fighters_df, left_on='fighter_1_1', right_on='Name', suffixes=('', '_fighter1'))

# Merge additional attributes for fighter_2_1
final_merged_df = pd.merge(merged_with_fighter1, fighters_df, left_on='fighter_2_1', right_on='Name', suffixes=('', '_fighter2'))
final_merged_df.to_csv('/Users/kevinliu/Desktop/UFC-Prediction-NN/data/creating-the-final-dataset/final_merged_fight_stats.csv', index=False)
