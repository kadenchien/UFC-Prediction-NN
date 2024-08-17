import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load your dataset
df = pd.read_csv('C:\Users\Kaden\Documents\GitHub\UFC-Prediction-NN\data\creating-the-final-dataset\final_merged_fight_stats.csv')

# Specify the number of past fights to include in the sequence
N = 5

# List of columns that represent the current fight (to be removed)
current_fight_columns = [
    'fighter_1_knockdowns', 'fighter_2_knockdowns', 
    'fighter_1_ss', 'fighter_2_ss', 'fighter_1_ss_pct', 'fighter_2_ss_pct',
    'fighter_1_total_strikes', 'fighter_2_total_strikes', 'fighter_1_takedowns',
    'fighter_2_takedowns', 'fighter_1_takedown_pct', 'fighter_2_takedown_pct',
    'fighter_1_submission_attempts', 'fighter_2_submission_attempts', 
    'fighter_1_reverses', 'fighter_2_reverses', 'fighter_1_control', 'fighter_2_control',
    'fighter_1_head_ss', 'fighter_2_head_ss', 'fighter_1_body_ss', 'fighter_2_body_ss',
    'fighter_1_leg_ss', 'fighter_2_leg_ss', 'fighter_1_distance_ss', 'fighter_2_distance_ss',
    'fighter_1_clinch_ss', 'fighter_2_clinch_ss', 'fighter_1_ground_ss', 'fighter_2_ground_ss'
]

# Remove current fight columns
df = df.drop(columns=current_fight_columns)


# Create sequences for each fighter
def create_fight_sequences(df, fighter_col, N):
    sequences = []
    for fighter in df[fighter_col].unique():
        fighter_data = df[df[fighter_col] == fighter].sort_values('event')  # Sort by event to maintain chronological order
        if len(fighter_data) >= N:
            for i in range(len(fighter_data) - N + 1):
                sequences.append(fighter_data.iloc[i:i+N].drop(columns=[fighter_col, 'event']).values)
    return np.array(sequences)

# Create sequences for fighter 1 and fighter 2
fighter_1_sequences = create_fight_sequences(df, 'fighter_1', N)
fighter_2_sequences = create_fight_sequences(df, 'fighter_2', N)

# Combine sequences into one dataset
all_sequences = np.concatenate([fighter_1_sequences, fighter_2_sequences], axis=0)

# Labels (assuming you want to predict fighter_1_result_1)
# You'll need to create a target variable based on your specific label strategy
labels = []
for fighter in df['fighter_1'].unique():
    fighter_data = df[df['fighter_1'] == fighter].sort_values('event')
    if len(fighter_data) >= N:
        labels.extend(fighter_data['fighter_1_result'].iloc[N-1:].values)
        
for fighter in df['fighter_2'].unique():
    fighter_data = df[df['fighter_2'] == fighter].sort_values('event')
    if len(fighter_data) >= N:
        labels.extend(fighter_data['fighter_2_result'].iloc[N-1:].values)

labels = np.array(labels)

# Reshape (Keras may require 3D input for RNNs)
all_sequences = all_sequences.reshape(all_sequences.shape[0], N, -1)

# Print shapes to verify
print(f'Sequence shape: {all_sequences.shape}')
print(f'Labels shape: {labels.shape}')

# Now you have `all_sequences` and `labels` ready to be fed into your RNN model!
