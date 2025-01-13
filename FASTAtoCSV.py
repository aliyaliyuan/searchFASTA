import pandas as pd
import os

#Set up directories
INPUT = "/path/to/input/files"
OUTPUT = "/path/to/output/files"

# Create the output directory if it doesn't exist
os.makedirs(OUTPUT, exist_ok=True)

# Function to process a single FASTA file
def process_fasta(file_path):
    headers = []
    sequences = []
    with open(file_path, "r") as file:
        sequence = ""
        for line in file:
            line = line.strip()
            if line.startswith(">"):  # Header line
                if sequence:  # Save the previous sequence before starting a new one
                    sequences.append(sequence)
                    sequence = ""
                headers.append(line[1:])  # Remove the ">" from the header
            else:  # Sequence line
                sequence += line
        # Save the last sequence
        if sequence:
            sequences.append(sequence)
    # Create a DataFrame
    return pd.DataFrame({"Header": headers, "Sequence": sequences})

# Process all FASTA files in the input directory
for filename in os.listdir(INPUT):
    if filename.endswith(".fasta") or filename.endswith(".fa"):
        fasta_path = os.path.join(INPUT, filename)
        df = process_fasta(fasta_path)
        # Save to CSV (preserving the same base filename)
        csv_filename = f"{os.path.splitext(filename)[0]}.csv"
        df.to_csv(os.path.join(OUTPUT, csv_filename), index=False)
        print(f"Processed {filename} -> {csv_filename}")

print("Batch processing completed!")
