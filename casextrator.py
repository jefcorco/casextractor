#!/usr/bin/env python
"""Convert each row of the Xchange ticket CSV into a formatted file.
   Takes a single argument (filename.csv) located in same directory."""

import csv
import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
filename = path + "/" + sys.argv[1]

#fields = []
row = []
rows = []

# Read the CSV file
with open (filename, 'r') as csvfile:
    # create a csv reader object
    csvreader = csv.reader(csvfile)

    # extract column names from first row
    column = next(csvreader)

    # extract each data row, one-by-one, and write to file
    for row in csvreader:
        print(row[0])
        print(row[1],"\n")
        print(f"{column[4]}: {row[4]}")
        print(f"{column[5]}: {row[5]}")
        print(f"{column[3]}: {row[3]}")
        print(f"{column[6]}: {row[6]}")
        print(f"{column[7]}: {row[7]}")
        print(f"{column[8]}: {row[8]}\n")
        print("Description")
        print(row[2])
        print()
        print("Updates")
        print(row[9])
        print("\n---------------------\n")
        
