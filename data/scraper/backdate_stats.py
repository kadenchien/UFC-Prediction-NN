import pandas as pd

# Load the CSV files
df_fighter1 = pd.read_csv(r'C:\Users\Kaden\Documents\GitHub\UFC-Prediction-NN\data\scraper\list1.csv')
df_fighter2 = pd.read_csv(r'C:\Users\Kaden\Documents\GitHub\UFC-Prediction-NN\data\scraper\list2.csv')

# Combine the dataframes for both fighters
df_combined = pd.concat([df_fighter1, df_fighter2], ignore_index=True)

# Sort by event (assuming event represents the chronological order)
df_combined.sort_values(by=['event'], inplace=True)

# Initialize dictionaries to store cumulative stats for each fighter
fighter_stats_1 = {}
fighter_stats_2 = {}

# Create new columns to store historical stats
for fighter_prefix in ['fighter_1', 'fighter_2']:
    df_combined[f'{fighter_prefix}_prev_stats'] = None

# Function to accumulate stats for a fighter
def accumulate_stats(fighter, stats_dict, row, fighter_prefix):
    # Initialize stats if the fighter is not in the dictionary
    if fighter not in stats_dict:
        stats_dict[fighter] = {
            'knockdowns': 0,
            'ss': 0,
            'ss_pct': 0,
            'total_strikes': 0,
            'takedowns': 0,
            'takedown_pct': 0,
            'submission_attempts': 0,
            'reverses': 0,
            'control': 0,
            'head_ss': 0,
            'body_ss': 0,
            'leg_ss': 0,
            'distance_ss': 0,
            'clinch_ss': 0,
            'ground_ss': 0
        }
    
    # Store the previous stats for the fighter
    prev_stats = stats_dict[fighter]
    df_combined.at[row.name, f'{fighter_prefix}_prev_stats'] = prev_stats.copy()
    
    # Update the fighter's stats with the current fight's stats
    for stat in prev_stats:
        prev_stats[stat] += row[f'{fighter_prefix}_{stat}']

# Iterate over each row in the sorted dataframe
for index, row in df_combined.iterrows():
    fighter_1 = row['fighter_1']
    fighter_2 = row['fighter_2']
    
    # Update stats for fighter_1
    accumulate_stats(fighter_1, fighter_stats_1, row, 'fighter_1')
    
    # Update stats for fighter_2
    accumulate_stats(fighter_2, fighter_stats_2, row, 'fighter_2')

# Save the updated DataFrame
df_combined.to_csv(r'C:\Users\Kaden\Documents\GitHub\UFC-Prediction-NN\data\scraper\processed_fights.csv', index=False)
