import pandas as pd
import os
from math import ceil

# Directories
input_dir = "csv_files/"
output_dir = "search_results/"
os.makedirs(output_dir, exist_ok=True)

# List of proteins
protein_list = ["protein_name_1", "protein_name_2", "specific_sequence"]  # Add your 288 proteins here

# Break protein list into chunks
def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

chunked_protein_lists = list(chunk_list(protein_list, 50))  # Adjust chunk size as needed

# Function to search CSV
def search_csv(file_path, protein_list):
    df = pd.read_csv(file_path)
    search_results = df[
        df["Header"].str.contains("|".join(protein_list), case=False, na=False) |
        df["Sequence"].str.contains("|".join(protein_list), case=False, na=False)
    ]
    return search_results

# Process files
combined_results = pd.DataFrame()
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_dir, filename)
        for chunk in chunked_protein_lists:
            results = search_csv(file_path, chunk)
            if not results.empty:
                results["Source_File"] = filename
                combined_results = pd.concat([combined_results, results], ignore_index=True)
        print(f"Processed {filename}")

# Save results
if not combined_results.empty:
    combined_results.to_csv(os.path.join(output_dir, "combined_search_results.csv"), index=False)
    print("Combined results saved to combined_search_results.csv")
else:
    print("No matches found.")
