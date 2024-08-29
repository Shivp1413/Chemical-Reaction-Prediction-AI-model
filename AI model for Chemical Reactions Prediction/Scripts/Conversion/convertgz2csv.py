import os
import json
import pandas as pd
from ord_schema.message_helpers import load_message
from ord_schema.proto import dataset_pb2
from google.protobuf.json_format import MessageToJson

# Define the folder containing .pb.gz files
data_folder = 'C:\\chai\\ord-data-main\\data\\00'  # Update this path to your local folder

# Create an empty list to store reaction data
reactions_data = []

# Loop through all .pb.gz files in the data folder
for file_name in os.listdir(data_folder):
    if file_name.endswith('.pb.gz'):
        file_path = os.path.join(data_folder, file_name)

        # Load the dataset from the Protobuf binary file
        try:
            dataset = load_message(file_path, dataset_pb2.Dataset)
            print(f"Successfully loaded {file_name}")
        except Exception as e:
            print(f"Failed to load {file_name}: {e}")
            continue

        # Iterate over each reaction in the dataset
        for rxn in dataset.reactions:
            try:
                # Convert the reaction to JSON format
                rxn_json = json.loads(
                    MessageToJson(
                        message=rxn,
                        including_default_value_fields=False,
                        preserving_proto_field_name=True
                    )
                )

                # Extract reaction metadata
                reaction_id = rxn_json.get('reaction_id', 'N/A')
                reaction_type = 'N/A'
                for identifier in rxn_json.get('identifiers', []):
                    if identifier.get('type') == 'NAME':
                        reaction_type = identifier.get('value', 'N/A')

                # Extract reactants, reagents, catalysts, solvents, and their roles
                reactants = []
                reagents = []
                catalysts = []
                solvents = []
                for input_key, input_value in rxn_json.get('inputs', {}).items():
                    for component in input_value.get('components', []):
                        smiles = ''
                        if 'identifiers' in component:
                            for identifier in component['identifiers']:
                                if identifier['type'] == 'SMILES':
                                    smiles = identifier['value']
                        role = component.get('reaction_role', 'UNKNOWN')
                        # Categorize based on the role
                        if role == 'REACTANT':
                            reactants.append(smiles)
                        elif role == 'REAGENT':
                            reagents.append(smiles)
                        elif role == 'CATALYST':
                            catalysts.append(smiles)
                        elif role == 'SOLVENT':
                            solvents.append(smiles)

                # Extract conditions
                temperature = 'N/A'
                if 'conditions' in rxn_json and 'temperature' in rxn_json['conditions']:
                    temp = rxn_json['conditions']['temperature'].get('setpoint', {})
                    temperature = f"{temp.get('value', 'N/A')} {temp.get('units', 'N/A')}"

                # Extract procedural notes
                procedure_details = 'N/A'
                if 'notes' in rxn_json and 'procedure_details' in rxn_json['notes']:
                    procedure_details = rxn_json['notes']['procedure_details']

                # Extract products and yields
                products = []
                yields = []
                for outcome in rxn_json.get('outcomes', []):
                    for product in outcome.get('products', []):
                        if 'identifiers' in product:
                            for identifier in product['identifiers']:
                                if identifier['type'] == 'SMILES':
                                    products.append(identifier['value'])
                        # Extract yield information
                        for measurement in product.get('measurements', []):
                            if measurement['type'] == 'YIELD':
                                yield_value = measurement.get('percentage', {}).get('value', 'N/A')
                                yields.append(str(yield_value))

                # Combine extracted data into a structured format
                reactions_data.append({
                    'Reaction ID': reaction_id,
                    'Reaction Type': reaction_type,
                    'Reactants': '.'.join(reactants) if reactants else 'N/A',
                    'Reagents': '.'.join(reagents) if reagents else 'N/A',
                    'Catalysts': '.'.join(catalysts) if catalysts else 'N/A',
                    'Solvents': '.'.join(solvents) if solvents else 'N/A',
                    'Products': '.'.join(products) if products else 'N/A',
                    'Yields (%)': ', '.join(yields) if yields else 'N/A',
                    'Temperature': temperature,
                    'Procedure Details': procedure_details
                })

            except Exception as e:
                print(f"Failed to process a reaction in {file_name}: {e}")

# Convert the list of reaction data into a DataFrame
df = pd.DataFrame(reactions_data)

# Save the DataFrame to a CSV file
output_csv_path = 'reaction_data.csv'
df.to_csv(output_csv_path, index=False)
print(f"Data extraction completed and saved as {output_csv_path}.")
