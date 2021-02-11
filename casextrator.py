#!/usr/bin/env python
"""Convert each row of the Xchange ticket CSV into a formatted file.
   Takes a single argument (filename.csv) located in same directory."""

import csv
import os
import sys
csv.field_size_limit(sys.maxsize)


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

# Check for filename argument
try:
    sys.argv[1]
except IndexError:
    print("casextractor: usage error: csv filename required")
    sys.exit(1)

# Get path and filename
path = os.path.dirname(os.path.abspath(__file__))
filename = sys.argv[1]
pathFilename = path + "/" + filename

# Read the CSV file
with open (pathFilename, 'r') as csvfile:
    # create a csv reader object
    csvreader = csv.reader(csvfile)

    # extract column names from first row
    column = next(csvreader)
    
    print(f"Writing text files from {filename}:")

    # extract each data row, one-by-one, and write to file
    i = 0
    for row in csvreader:
        print(f"{i}: {row[0]}.txt")
        i = i + 1

        txtFilenamePath = "txt/" + row[0] + ".txt"        

        if not os.path.exists(os.path.dirname(txtFilenamePath)):
            try:
                os.makedirs(os.path.dirname(txtFilenamePath))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(txtFilenamePath, mode="w", encoding="utf-8") as f:
            f.write(f"{row[0]}\n")
            f.write(f"{deamp(row[1])}\n\n")
            f.write(f"{column[4]}: {row[4]}\n")
            f.write(f"Customer Priority: {row[5]}\n")
            f.write(f"{column[3]} Email: {row[3]}\n")
            f.write(f"Created: {row[6]}\n")
            f.write(f"{column[7]}: {row[7]}\n")
            f.write(f"{column[8]}: {row[8]}\n\n")
            f.write("Description\n===========\n")
            f.write(f"{deamp(row[2])}\n\n")
            f.write("Comments\n========\n")
            f.write(f"{deamp(row[9])}\n")
            
 