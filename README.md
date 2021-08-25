# casextractor
Convert each row of the Xchange ticket CSV into a formatted file

I created this tool to assist with the transition of BroadSoft customers from the Xchange platform to Cisco SCM. BroadSoft customers are able to download their complete Xchange/JIRA ticket history in a single CSV format via Xchange (Ticketing>Gear icon>Export all tickets as CSV). To create a more readable format, I created this python script that converts each row of the CSV to a plain text file and a formatted HTML file (each with the same data contents).  The HTML files are formatted similarly to what customers would see in Xchange. The script also looks for text denoted as “code” and formats this with a fixed-width font and puts dividers between updates/comments to increase readability. Because each ticket is in an individual file, the indexing service of the users desktop can be used to search for keywords and locate the desired ticket.

To use the tool, run the python script with the CSV in the same directory. Two subdirectories will be created, txt and html. Note that the ticketformat.htm is also required and acts as a template for the resulting html document.
