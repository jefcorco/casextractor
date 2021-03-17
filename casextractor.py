"""Convert each row of the Xchange ticket CSV into a formatted file.
   Takes a single argument (filename.csv) located in same directory."""

import csv
import os
import sys
import re
from string import Template

# Set the field size limit to avoid "_csv.Error: field larger than field limit (131072)"
csv.field_size_limit(sys.maxsize)


# Function to remove escaped characters from text
def deAmp(t):
    # See if there is any &amp text
    if t.find('&amp') != -1:
        # There is so clean up all known replacements
        t = t.replace('&amp;quot;', '\"')
        t = t.replace('&#039;', '\'')
        t = t.replace('&amp;lt;', '<')
        t = t.replace('&amp;gt;', '>')
        t = t.replace('&amp;amp;', '&')
    return t

# Function to replace new lines with html breaks so the paragraphs don't all run together in the html file
def addBreaks(t):
    t = t.replace('\n', '<br />')
    return t

# Function to replace {code} with the html <pre> tags

def codePre(t):
    # A simple search and replace won't suffice since the ending {code} is just like the first
    # Instead chunk it up by splitting on the string {code}
    # But because the opening delimiter might also be {code:java} I can't just use splitText  = t.split('{code}')
    # The regular expression (re) library has been imported and the following can be used.
    splitText  = re.split('{code}|{code:java}|{noformat}',t)
    for count,chunk in enumerate(splitText):
        if count % 2 != 0:
            splitText[count] = "<pre>" + splitText[count] + "</pre>"
    # Recombine into a single string and return    
    return "".join(splitText)
    
# Function to add an html line (<hr>) wherever there was an update--just before the text "";[updated"
def addLine(t):
    t = t.replace('; [updated','<hr>; [updated')
    return t

# Get path and filename
path = os.path.dirname(os.path.abspath(__file__))

# Check for filename argument
try:
    sys.argv[1]
except IndexError:
    print("casextractor: usage error: csv filename required")
    filename = "xchange2.csv"
    #sys.exit(1)
else:
    filename = sys.argv[1]


pathFilename = path + "/" + filename

# Read in the html template file for later use
# ticketformat.htm is hardcoded, but this could be made an argument later.
with open ("ticketformat.htm", 'r') as h:
    docTemplate = h.read()

# Read the CSV file
with open (pathFilename, 'r') as csvfile:
    # create a csv reader object
    csvreader = csv.reader(csvfile)

    # extract column names from first row
    column = next(csvreader)
    
    print(f"Writing files from {filename}:")

    # extract each data row, one-by-one, and write to file
    # the i iterator is just to print the current file it's working on
    i = 0
    for row in csvreader:
        print(f"{i}: {row[0]}.txt")
        txtFilenamePath = "txt/" + row[0] + ".txt"        

        if not os.path.exists(os.path.dirname(txtFilenamePath)):
            try:
                os.makedirs(os.path.dirname(txtFilenamePath))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        
        # Write out the text file for the row
        with open(txtFilenamePath, mode="w", encoding="utf-8") as f:
            f.write(f"{row[0]}\n")
            f.write(f"{deAmp(row[1])}\n\n")
            f.write(f"{column[4]}: {row[4]}\n")
            f.write(f"Customer Priority: {row[5]}\n")
            f.write(f"{column[3]} Email: {row[3]}\n")
            f.write(f"Created: {row[6]}\n")
            f.write(f"{column[7]}: {row[7]}\n")
            f.write(f"{column[8]}: {row[8]}\n\n")
            f.write("Description\n===========\n")
            f.write(f"{deAmp(row[2])}\n\n")
            f.write("Comments\n========\n")
            f.write(f"{deAmp(row[9])}\n")

        # Write out the html file for the row
        htmlFilenamePath = path + "/html/" + row[0] + ".htm"

        if not os.path.exists(os.path.dirname(htmlFilenamePath)):
            try:
                os.makedirs(os.path.dirname(htmlFilenamePath))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        
        print(f"{i}: {row[0]}.htm")
        i += 1
        temp = "first row\r\nsecond row"
        with open (htmlFilenamePath, 'w') as h:
            s = Template(docTemplate)
            h.write(s.substitute(\
                ID=row[0],\
                Title=deAmp(row[1]),\
                Severity=row[4],\
                Priority=row[5],\
                Contact=row[3],\
                Created=row[6],\
                Updated=row[7],\
                Status=row[8],\
                Description=codePre(addBreaks(deAmp(row[2]))),\
                Updates=codePre(addLine(addBreaks(deAmp(row[9]))))))
            
