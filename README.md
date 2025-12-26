1. Write a Python program to extract product information from mdcomputers.in for a given search term.For example, this URL shows results for “external hard drives”:
mdcomputers.in/?route=product/search&search=external harddrive
The program should:
- Accept a search term as input
- Fetch the search results page
- Output the listed products (images not required) in any format of your choice
Extra points if you detail the design choices and output format choices made.
2. The following questions test your aptitude for interacting with databases. The questions are based off the following public SQL DB: docs.rfam.org/en/latest/database.html
a) How many types of Acacia plants can be found in the taxonomy table of the dataset?
b) Which type of wheat has the longest DNA sequence? (hint: use the rfamseq and the taxonomy tables)
c) We want to paginate a list of the family names and their longest DNA sequence lengths (in descending order of length) where only families that have DNA sequence lengths greater than 1,000,000 are included. Give a query that will return the 9th page when there are 15 results per page. (hint: we need the family accession ID, family name and the maximum length in the results)

3. This question is to test your aptitude for writing small shell scripts on Unix. You are provided this URL: raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data… which has data on a few companies. Write a shell script that will take this URL as input and output the following: company name, location and founding year; the output must be sorted by founding year.
