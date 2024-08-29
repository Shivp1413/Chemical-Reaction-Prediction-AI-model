# Import necessary modules from the ORD (Open Reaction Database) schema
from ord_schema.message_helpers import load_message, write_message
from ord_schema.proto import dataset_pb2
import random

# Define the path to the input .pb.gz file (Protocol Buffer with Gzip compression).
# This file is assumed to be in a binary format specific to the Open Reaction Database.
# Update this path to point to the actual location of your file.
input_fname = "C:\\chai\\ord-data-main\\data\\00\\ord_dataset-00005539a1e04c809a9a78647bea649c.pb.gz"

# Define output file names for the training and testing datasets in Protocol Buffer Text Format.
output_train_fname = "train_sample_file.pbtxt"
output_test_fname = "test_sample_file.pbtxt"

# Load the dataset from the .pb.gz file into a Dataset protocol buffer object.
# The load_message function handles the deserialization of the binary file.
dataset = load_message(input_fname, dataset_pb2.Dataset)

# Convert the dataset into a list of individual reactions.
# Each reaction represents a single experimental entry in the dataset.
reactions = list(dataset.reactions)

# Randomly shuffle the reactions to ensure a random distribution between training and test sets.
random.shuffle(reactions)

# Define the split ratio for training and test datasets.
# Here, 80% of the reactions will be used for training and 20% for testing.
split_ratio = 0.8
split_index = int(len(reactions) * split_ratio)

# Split the reactions into training and test sets based on the split index.
train_reactions = reactions[:split_index]
test_reactions = reactions[split_index:]

# Create two new Dataset protocol buffer objects for training and testing.
train_dataset = dataset_pb2.Dataset()
train_dataset.reactions.extend(train_reactions)

test_dataset = dataset_pb2.Dataset()
test_dataset.reactions.extend(test_reactions)

# Write the training dataset to a .pbtxt file in Protocol Buffer Text Format.
write_message(train_dataset, output_train_fname)

# Write the testing dataset to a .pbtxt file in Protocol Buffer Text Format.
write_message(test_dataset, output_test_fname)

# Print messages indicating where the training and testing datasets were saved.
print(f"Training data saved to {output_train_fname}")
print(f"Test data saved to {output_test_fname}")
