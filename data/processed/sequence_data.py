import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv(r'C:\Users\Kaden\Documents\GitHub\UFC-Prediction-NN\data\processed\processed_ufc_dataset.csv')

# Function to convert a single value to float, handling NaN and empty values
def safe_float_convert(value):
    if pd.isna(value) or value == '':
        return 0.0
    try:
        return float(value)
    except ValueError:
        return 0.0

# Function to create a sequence matrix from a list of lists
def create_sequence_matrix(data_lists):
    # Convert each list to a numpy array, replacing NaN and empty values with 0
    arrays = []
    for lst in data_lists:
        # Convert string representation of list to actual list
        if isinstance(lst, str):
            lst = lst.strip('[]').split(',')
        # Convert each value in the list, handling NaN and empty values
        arr = np.array([safe_float_convert(val) for val in lst])
        arrays.append(arr.reshape(-1, 1))
    
    # Find the maximum length among all arrays
    max_len = max(arr.shape[0] for arr in arrays)
    
    # Pad shorter arrays with zeros
    padded_arrays = [np.pad(arr, ((0, max_len - arr.shape[0]), (0, 0)), 'constant') for arr in arrays]
    
    # Stack the arrays horizontally
    return np.hstack(padded_arrays)

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

# Create sequence matrices and add them to the DataFrame
fighter1_sequences = []
fighter2_sequences = []

for _, row in df.iterrows():
    fighter1_data = [row[f'{stat}'] for stat in previous_fight_stats_fighter_1]
    fighter1_sequence = create_sequence_matrix(fighter1_data)
    fighter1_sequences.append(fighter1_sequence)

    fighter2_data = [row[f'{stat}'] for stat in previous_fight_stats_fighter_2]
    fighter2_sequence = create_sequence_matrix(fighter2_data)
    fighter2_sequences.append(fighter2_sequence)

# Add the sequence matrices to the DataFrame
df['fighter_1_history_sequence'] = fighter1_sequences
print(fighter1_sequences)
df['fighter_2_history_sequence'] = fighter2_sequences
print(fighter2_sequences)

# Now the DataFrame has two new columns: 'fighter_1_history_sequence' and 'fighter_2_history_sequence'
# Each cell in these columns contains a numpy array representing the fighter's history sequence
df.to_csv("final.csv")

# If you want to save the DataFrame with sequences, it's better to use pickle:
#import pickle

#with open('ufc_fights_with_sequences.pkl', 'wb') as f:
    #pickle.dump(df, f)

# To load the DataFrame later:
# with open('ufc_fights_with_sequences.pkl', 'rb') as f:
#     df_loaded = pickle.load(f)