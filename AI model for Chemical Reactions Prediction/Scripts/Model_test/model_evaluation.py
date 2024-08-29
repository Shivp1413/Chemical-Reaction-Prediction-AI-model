from model1 import parse_pbtxt  # Import the parse_pbtxt function
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd

# Load the trained model
model = load_model("trained_model.h5")

# Load and preprocess the test data
test_data = parse_pbtxt("test_sample_file.pbtxt")  # Ensure the test file path is correct

# Handle missing values by dropping rows with NaNs in temperature or yield
test_data.dropna(subset=['temperature', 'yield'], inplace=True)

# Encoding categorical features using the same encoder used in training
le = LabelEncoder()
test_data['reaction_type_encoded'] = le.fit_transform(test_data['reaction_type'])

# Scaling numerical features using the same scaler used in training
scaler = StandardScaler()
test_data[['temperature', 'yield']] = scaler.fit_transform(test_data[['temperature', 'yield']])

# Extract features and target from test data
X_test = test_data[['reaction_type_encoded', 'temperature']].values
y_test = test_data['yield'].values

# Evaluate the model on the test set
test_loss, test_mae = model.evaluate(X_test, y_test)
print(f"Test Loss: {test_loss}, Test MAE: {test_mae}")
