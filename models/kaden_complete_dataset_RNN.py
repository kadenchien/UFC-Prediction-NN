import tensorflow as tf
from tensorflow.keras.models import Model
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout, Concatenate, Bidirectional
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
from sklearn.model_selection import KFold

# Load the DataFrame with sequences
with open(r'C:\Users\Kaden\Documents\GitHub\UFC-Prediction-NN\data\processed\ufc_fights_with_sequences.pkl', 'rb') as f:
    df = pickle.load(f)

# Function to pad sequences
def pad_sequence(seq, max_length):
    return pad_sequences([seq], maxlen=max_length, padding='post', truncating='post')[0]

# Find the maximum sequence length
max_length = max(
    max(len(seq) for seq in df['fighter_1_history_sequence']),
    max(len(seq) for seq in df['fighter_2_history_sequence'])
)

# Pad sequences
df['fighter_1_history_sequence'] = df['fighter_1_history_sequence'].apply(lambda x: pad_sequence(x, max_length))
df['fighter_2_history_sequence'] = df['fighter_2_history_sequence'].apply(lambda x: pad_sequence(x, max_length))

# Prepare sequence data
X_seq = np.array(df['fighter_1_history_sequence'].tolist() + df['fighter_2_history_sequence'].tolist())

# Prepare additional features
additional_features = [
    'Wins', 'Losses', 'Draws', 'Style_Boxing', 'Style_Brawler', 'Style_Brazilian Jiu-Jitsu',
    'Style_Freestyle', 'Style_Grappler', 'Style_Jiu-Jitsu', 'Style_Judo',
    'Style_Karate', 'Style_Kickboxer', 'Style_Kung Fu', 'Style_Kung-Fu',
    'Style_MMA', 'Style_Muay Thai', 'Style_Sambo', 'Style_Striker',
    'Style_Wrestler', 'Style_Wrestling', 'Style_Taekwondo', 'Age', 'Height',
    'Reach'
]

# Concatenate features for both fighters
X_additional = pd.concat([
    df[additional_features],
    df[[col + '_fighter2' for col in additional_features]].rename(columns=lambda x: x.replace('_fighter2', ''))
])

# Convert to numpy array and normalize
scaler = StandardScaler()
X_additional = scaler.fit_transform(X_additional)

# Convert 'W' to 1 and 'L' to 0
df['fighter_1_result_numeric'] = df['fighter_1_result_1'].map({'W': 1, 'L': 0})
print(df['fighter_1_result_numeric'].sum())

# Prepare labels
y = np.concatenate([df['fighter_1_result_numeric'].values, 1 - df['fighter_1_result_numeric'].values])

# Split the data
X_seq_train, X_seq_test, X_add_train, X_add_test, y_train, y_test = train_test_split(
    X_seq, X_additional, y, test_size=0.2, random_state=42
)

# Define model parameters
seq_input_shape = (X_seq_train.shape[1], X_seq_train.shape[2])
add_input_shape = X_add_train.shape[1]
lstm_units = 128
dense_units = 64
dropout_rate = 0.2

# Define inputs
seq_input = Input(shape=seq_input_shape, name='sequence_input')
add_input = Input(shape=(add_input_shape,), name='additional_input')

# Sequence branch
x = Bidirectional(LSTM(lstm_units, return_sequences=True))(seq_input)
x = Dropout(dropout_rate)(x)
x = Bidirectional(LSTM(lstm_units, return_sequences=True))(x)
x = Dropout(dropout_rate)(x)
x = Bidirectional(LSTM(lstm_units))(x)

# Additional features branch
from tensorflow.keras.regularizers import l2
y = Dense(dense_units, activation='relu', kernel_regularizer=l2(0.01))(add_input)
y = Dropout(dropout_rate)(y)

from tensorflow.keras.callbacks import EarlyStopping

early_stopping = EarlyStopping(monitor='val_loss', patience=25, restore_best_weights=True)

# Combine branches
combined = Concatenate()([x, y])

# Output
output = Dense(dense_units, activation='relu')(combined)
output = Dropout(dropout_rate)(output)
output = Dense(1, activation='sigmoid')(output)

# Create model
model = Model(inputs=[seq_input, add_input], outputs=output)

# Compile model
model.compile(optimizer=Adam(learning_rate=0.0001), loss='binary_crossentropy', metrics=['accuracy'])

# Print model summary
model.summary()

# Define training parameters
epochs = 50
batch_size = 32

# Train the model
history = model.fit(
    [X_seq_train, X_add_train], y_train,
    epochs=epochs,
    batch_size=batch_size,
    validation_split=0.2,
    callbacks=[early_stopping],
    verbose=1
)

# Evaluate the model on the test set
loss, accuracy = model.evaluate([X_seq_test, X_add_test], y_test, verbose=0)
print(f'Test loss: {loss:.4f}')
print(f'Test accuracy: {accuracy:.4f}')

# Make predictions
predictions = model.predict([X_seq_test, X_add_test])
predictions = (predictions > 0.5).astype(int)  # Convert probabilities to binary predictions