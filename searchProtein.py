import pandas as pd
import os

# Load CSV you created from FASTAtoCSV.py 
#The CSV has 2 columns - 'Header' and 'Sequence', you want to compare the items in the 'Sequence' column

FILE = '/path/to/csv'

try:
    df = pd.read_csv(FILE)
except FileNotFoundError:
    print(f"Error: File {FILE} not found.")
    exit()

# Check if the required column exists
COLUMN_NAME = 'Sequence'  
if COLUMN_NAME not in df.columns:
    print("Error: Specified column not found in the CSV.")
    exit()

# Extract column data from Sequence
FASTA_sequences = df['Sequence']

# List of sequences to find
#Replace "seq1", "seq2, and "seq3" with the protein sequences you are searching for 

sequenceList = ["seq1",
    "seq2",
    "seq3"
	]

# Longest Prefix Sequence function (for the Search algorithm)
def LPS(sequenceOfInterest):
    m = len(sequenceOfInterest)
    lps = [0] * m
    j = 0
    i = 1

    while i < m:
        if sequenceOfInterest[i] == sequenceOfInterest[j]:
            j += 1
            lps[i] = j
            i += 1
        else:
            if j != 0:
                j = lps[j-1]
            else:
                lps[i] = 0
                i += 1
    return lps


# KMPSearch function
def KMPSearch(FASTAprotein, sequenceOfInterest,output):
    n = len(FASTAprotein)
    m = len(sequenceOfInterest)
    lps = LPS(sequenceOfInterest)
    i = j = 0

    while i < n:
        if sequenceOfInterest[j] == FASTAprotein[i]:
            i += 1
            j += 1

        if j == m:
            output.write(f"{sequenceOfInterest} found at index: {i - j}\n", )
            j = lps[j-1]
        elif i < n and sequenceOfInterest[j] != FASTAprotein[i]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1


#Writes results to a .txt file 
#Replace /path/to/directory to where you want the output to go 
OUTPUT = f'/path/to/directory/{os.path.splitext(os.path.basename(FILE))[0]}_output.txt'


# Iterate through each protein in the FASTA column and search for sequences
with open(OUTPUT, 'w') as output_file:
    for seq in sequenceList:
        for index, row in df.iterrows():
            FASTAprotein = row.iloc[1]  
            KMPSearch(FASTAprotein, seq, output_file)

print(f"Results written to {OUTPUT}")




