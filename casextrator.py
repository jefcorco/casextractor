#!/usr/bin/env python
"""Convert each row of the Xchange ticket CSV into a formatted file.
   Takes a single argument (filename.csv) located in same directory."""

import csv
import os
import sys

def deamp(text):
    # See if there is any &amp text
    if text.find('&amp') != -1:
        # There is so clean up all known replacements
        text = text.replace('&amp;quot;', '\"')
        text = text.replace('&#039;', '\'')
        text = text.replace('&amp;lt;', '<')
        text = text.replace('&amp;gt;', '>')
        text = text.replace('&amp;amp;', '&')
    return text

path = os.path.dirname(os.path.abspath(__file__))
filename = path + "/" + sys.argv[1]

# Read the CSV file
with open (filename, 'r') as csvfile:
    # create a csv reader object
    csvreader = csv.reader(csvfile)

    # extract column names from first row
    column = next(csvreader)

    # extract each data row, one-by-one, and write to file
    for row in csvreader:
        print(row[0])
        print(deamp(row[1]),"\n")
        print(f"{column[4]}: {row[4]}")
        print(f"Customer Priority: {row[5]}")
        print(f"{column[3]} Email: {row[3]}")
        print(f"Created: {row[6]}")
        print(f"{column[7]}: {row[7]}")
        print(f"{column[8]}: {row[8]}\n")
        print("Description")
        print(deamp(row[2]))
        print()
        print("Comments")
        print(deamp(row[9]))
        print("\n---------------------\n")
        
