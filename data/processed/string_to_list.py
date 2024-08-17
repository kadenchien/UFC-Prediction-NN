import pandas as pd
import numpy as np
import pickle

# Read the CSV file
df = pd.read_csv(r'C:\Users\Kaden\Documents\GitHub\UFC-Prediction-NN\data\creating-the-final-dataset\prepped_data_for__ML.csv')

# Function to convert a single value to float, handling NaN and empty values
def safe_float_convert(value):
    if pd.isna(value) or value == '':
        return 0.0
    try:
        return float(value)
    except ValueError:
        return 0.0

# Function to convert a cell from string to a NumPy array
def convert_cell_to_array(cell_value):
    if isinstance(cell_value, str):
        cell_value = cell_value.strip('[]').split(',')
    return np.array([safe_float_convert(val) for val in cell_value])

# List of statistics you want to include
previous_fight_stats_fighter_1 = [
    'fighter_1_knockdowns_previous', 'fighter_1_ss_previous', 'fighter_1_ss_pct_previous',
    'fighter_1_total_strikes_previous', 'fighter_1_takedowns_previous', 'fighter_1_takedown_pct_previous',
    'fighter_1_submission_attempts_previous', 'fighter_1_reverses_previous', 'fighter_1_control_previous',
    'fighter_1_head_ss_previous', 'fighter_1_body_ss_previous', 'fighter_1_leg_ss_previous',
    'fighter_1_distance_ss_previous', 'fighter_1_clinch_ss_previous', 'fighter_1_ground_ss_previous'
]

previous_fight_stats_fighter_2 = [
    'fighter_2_knockdowns_previous', 'fighter_2_ss_previous', 'fighter_2_ss_pct_previous',
    'fighter_2_total_strikes_previous', 'fighter_2_takedowns_previous', 'fighter_2_takedown_pct_previous',
    'fighter_2_submission_attempts_previous', 'fighter_2_reverses_previous', 'fighter_2_control_previous',
    'fighter_2_head_ss_previous', 'fighter_2_body_ss_previous', 'fighter_2_leg_ss_previous',
    'fighter_2_distance_ss_previous', 'fighter_2_clinch_ss_previous', 'fighter_2_ground_ss_previous'
]

# Convert cells in specified columns to NumPy arrays
for col in previous_fight_stats_fighter_1 + previous_fight_stats_fighter_2:
    df[col] = df[col].apply(convert_cell_to_array)

# Save the modified DataFrame using pickle
with open('ufc_fights_3700_final.pkl', 'wb') as f:
    pickle.dump(df, f)

# To load the DataFrame later:
# with open('ufc_fights_with_sequences.pkl', 'rb') as f:
#     df_loaded = pickle.load(f)
