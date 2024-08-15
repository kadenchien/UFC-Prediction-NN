import pandas as pd

df = pd.read_csv(r'C:\Users\Kaden\Documents\GitHub\UFC-Prediction-NN\data\scraper\list2.csv', header=0)

# Assuming the DataFrame is sorted with fighter_1 in alphabetical order and fights in chronological order
def add_previous_stats(df):
    # Create a list of all columns related to fighter_1 stats
    fighter_2_columns = [
        'fighter_2_knockdowns', 'fighter_2_ss', 'fighter_2_ss_pct', 'fighter_2_total_strikes',
        'fighter_2_takedowns', 'fighter_2_takedown_pct', 'fighter_2_submission_attempts',
        'fighter_2_reverses', 'fighter_2_control', 'fighter_2_head_ss', 'fighter_2_body_ss',
        'fighter_2_leg_ss', 'fighter_2_distance_ss', 'fighter_2_clinch_ss', 'fighter_2_ground_ss'
    ]

    # Create new columns for previous stats
    for col in fighter_2_columns:
        df[f'{col}_previous'] = None

    # Process each fighter's fights
    for fighter in df['fighter_2'].unique():
        # Filter the DataFrame for the current fighter
        fighter_df = df[df['fighter_2'] == fighter]
        
        # Initialize previous stats
        previous_stats = {col: [] for col in fighter_2_columns}
        
        for index, row in fighter_df.iterrows():
            for col in fighter_2_columns:
                df.at[index, f'{col}_previous'] = previous_stats[col].copy()
                # Append current stats to the previous_stats for future use
                previous_stats[col].append(row[col])
    
    return df

# Apply the function to your DataFrame
df = add_previous_stats(df)

# Save or further process your updated DataFrame
df.to_csv('list2_full.csv', index=False)
