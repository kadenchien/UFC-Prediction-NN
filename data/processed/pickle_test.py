import pickle
import pandas as pd

# Load the DataFrame from the pickle file
with open('ufc_fights_with_sequences.pkl', 'rb') as f:
    df = pickle.load(f)

# Print basic information about the DataFrame
print("DataFrame Info:")
print(df.info())

# Print the first few rows of the DataFrame
print("\nFirst few rows:")
print(df.head())

# Print column names
print("\nColumn names:")
print(df.columns)

# Check the content of the sequence columns
print("\nExample of fighter_1_history_sequence:")
print(df['fighter_1_1'].iloc[4])
print(df['fighter_1_history_sequence'].iloc[4])

print("\nExample of fighter_2_history_sequence:")
print(df['fighter_2_history_sequence'].iloc[5])

# Print some statistics
print("\nDataFrame description:")
print(df.describe())

# Check for any null values
print("\nNull values in DataFrame:")
print(df.isnull().sum())

# If you want to check a specific row in more detail
row_index = 0  # Change this to check different rows
print(f"\nDetailed view of row {row_index}:")
for column in df.columns:
    print(f"{column}:")
    print(df[column].iloc[row_index])
    print()