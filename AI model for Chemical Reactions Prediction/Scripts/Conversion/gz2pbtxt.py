# Import necessary modules from the ORD (Open Reaction Database) schema
from ord_schema.message_helpers import load_message, write_message
from ord_schema.proto import dataset_pb2

# Define the path to the input .pb.gz file (Protocol Buffer with Gzip compression).
# This file is assumed to be in a binary format specific to the Open Reaction Database.
# Change the file path below to point to the actual location of your file.
input_fname = "C:\\chai\\ord-data-main\\data\\00\\ord_dataset-00005539a1e04c809a9a78647bea649c.pb.gz"

# Define the output file name.
# This will be a human-readable text file in the Protocol Buffer Text Format.
output_fname = "sample_file.pbtxt"

# Load the dataset from the .pb.gz file into a Dataset protocol buffer object.
# The load_message function handles the deserialization of the binary file.
dataset = load_message(input_fname, dataset_pb2.Dataset)

# Write the Dataset protocol buffer object to a text file in the Protocol Buffer Text Format.
# This allows for easy reading and inspection of the data.
write_message(dataset, output_fname)

# Print a message indicating successful conversion and output file location.
print(f"Converted {input_fname} to {output_fname}")
