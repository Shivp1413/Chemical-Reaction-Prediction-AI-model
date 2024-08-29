import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pandas as pd
import numpy as np
import re

# Function to parse the .pbtxt file and extract relevant data
def parse_pbtxt(file_path):
    reactions = []
    with open(file_path, 'r') as file:
        content = file.read()

    # Extracting each reaction block
    reaction_blocks = content.split("reactions {")[1:]
    
    for block in reaction_blocks:
        # Extracting the reaction type, conditions, reactants, and yield
        reaction = {}

        # Extracting reaction type
        reaction_type = re.search(r'value: "(.*?) \[.*?\]', block)
        reaction['reaction_type'] = reaction_type.group(1) if reaction_type else 'Unknown'

        # Extracting SMILES strings and roles
        smiles = re.findall(r'type: SMILES\s+value: "(.*?)"', block)
        roles = re.findall(r'reaction_role: (REAGENT|REACTANT|CATALYST|SOLVENT|PRODUCT)', block)
        reaction['smiles'] = smiles
        reaction['roles'] = roles

        # Extracting yield
        yield_value = re.search(r'percentage {\s+value: (\d+\.\d+)', block)
        reaction['yield'] = float(yield_value.group(1)) if yield_value else np.nan
        
        # Adjusted regex to extract temperature setpoints
        temp = re.search(r'temperature\s*{\s*setpoint\s*{\s*value:\s*([\d.]+)', block)
        reaction['temperature'] = float(temp.group(1)) if temp else np.nan

        reactions.append(reaction)

    return pd.DataFrame(reactions)

# Load and preprocess the data
data = parse_pbtxt("sample_file.pbtxt")

# Print the first few rows to inspect the data
print("Parsed Data:\n", data.head())

# Check if the data has missing values
print("\nMissing Values:\n", data.isnull().sum())

# Handle missing values by dropping rows with NaNs in temperature or yield
data.dropna(subset=['temperature', 'yield'], inplace=True)

# Check if data is empty after dropping NaNs
if data.empty:
    print("Data is empty after dropping missing values. Check data extraction logic.")
else:
    # Encoding categorical features
    le = LabelEncoder()
    data['reaction_type_encoded'] = le.fit_transform(data['reaction_type'])

    # Scaling numerical features
    scaler = StandardScaler()
    data[['temperature', 'yield']] = scaler.fit_transform(data[['temperature', 'yield']])

    # Splitting features and target
    X = data[['reaction_type_encoded', 'temperature']].values
    y = data['yield'].values

    # Defining a simple neural network model
    model = Sequential([
        Input(shape=(X.shape[1],)),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dense(1)  # Output layer for regression
    ])

    # Compiling the model
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    # Training the model
    model.fit(X, y, epochs=50, batch_size=16, validation_split=0.2)

    # Save the trained model
    model.save("trained_model.h5")
