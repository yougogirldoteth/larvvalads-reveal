import pandas as pd
import json
import os
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--seed", help="The block hash", required=True)
args = parser.parse_args()

random.seed(args.seed)

metadata_df = pd.read_csv('./metadata.csv')

# mapping from renaming GIFs before
with open('mapping.json', 'r') as f:
    mapping = json.load(f)

reversed_mapping = {value: key for key, value in mapping.items()}

output_directory = './json'

# shuffled list of token numbers based on seed
token_numbers = list(range(1, len(metadata_df) + 1))
random.shuffle(token_numbers)


def create_json_files(df, reversed_mapping, output_dir, token_numbers):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for index, row in df.iterrows():
        original_filename_with_extension = row['original_filename']

        if original_filename_with_extension not in reversed_mapping:
            print(f"No mapping found for {original_filename_with_extension}. Skipping...")
            continue

        new_filename = reversed_mapping[original_filename_with_extension]

        # JSON structure
        token_number = token_numbers[index]
        json_data = {
            "name": f"Larvva Lad #{token_number}",
            "description": row['description'],
            "image": f"ipfs://bafybeihg75tspwyn4cfaqdgih5r5tdvwjzl2r75n6nkfsmvutntovb22xm/{new_filename}",
            "attributes": []
        }

        # attributes
        attributes = ['type', 'headwear', 'eyes', 'accessory', '1/1', 'artist']
        for attr in attributes:
            if attr in row and pd.notnull(row[attr]):
                json_data['attributes'].append({
                    "value": row[attr],
                    "trait_type": attr.capitalize()
                })

        # saving file
        output_filename = os.path.join(output_dir, str(token_number))
        with open(output_filename, 'w') as f:
            json.dump(json_data, f, indent=4)
        print(f"Generated {output_filename}")

create_json_files(metadata_df, reversed_mapping, output_directory, token_numbers)
