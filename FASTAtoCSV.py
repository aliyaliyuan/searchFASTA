import pandas as pd

# Filepath to your FASTA file
fasta_file = "file.fasta"

# Initialize lists to hold headers and sequences
headers = []
sequences = []

# Go through FASTA file
with open(fasta_file, "r") as file:
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
df = pd.DataFrame({"Header": headers, "Sequence": sequences})

# Save to a CSV file for later use 
df.to_csv("parsed_fasta.csv", index=False)

print(df.head())  # View the first few rows
