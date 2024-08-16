import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv(r'C:\Users\Kaden\Documents\GitHub\UFC-Prediction-NN\data\processed\final_merged_fight_stats_final.csv')

# List of columns to drop that contain current fight stats
current_stats_columns = [
    'fighter_1_knockdowns_1', 'fighter_2_knockdowns_1', 
    'fighter_1_ss_1', 'fighter_2_ss_1', 
    'fighter_1_ss_pct_1', 'fighter_2_ss_pct_1', 
    'fighter_1_total_strikes_1', 'fighter_2_total_strikes_1',
    'fighter_1_takedowns_1', 'fighter_2_takedowns_1',
    'fighter_1_takedown_pct_1', 'fighter_2_takedown_pct_1',
    'fighter_1_submission_attempts_1', 'fighter_2_submission_attempts_1',
    'fighter_1_reverses_1', 'fighter_2_reverses_1',
    'fighter_1_control_1', 'fighter_2_control_1',
    'fighter_1_head_ss_1', 'fighter_2_head_ss_1',
    'fighter_1_body_ss_1', 'fighter_2_body_ss_1',
    'fighter_1_leg_ss_1', 'fighter_2_leg_ss_1',
    'fighter_1_distance_ss_1', 'fighter_2_distance_ss_1',
    'fighter_1_clinch_ss_1', 'fighter_2_clinch_ss_1',
    'fighter_1_ground_ss_1', 'fighter_2_ground_ss_1', 'original_order'
]

# Drop the current fight stats
df.drop(columns=current_stats_columns, inplace=True)

# Optional: Save the processed data
df.to_csv('processed_ufc_dataset.csv', index=False)

# The final step would be to convert these sequences into the right format for your RNN model,
# which could involve reshaping and padding as necessary.

print("Dataset has been processed and saved as 'processed_ufc_dataset.csv'")
