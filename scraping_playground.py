#%%
import requests
from bs4 import BeautifulSoup

# URL of the Formula 1 race results page
url = "https://www.formula1.com/en/results/2025/races"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')



# Print the table for now (to be processed further)
soup
#%%
# Find the race results table
race_results_table = soup.find('table')

# Extract headers
headers = [header.text.strip() for header in race_results_table.find_all('th')]

# Extract rows
rows = []
for row in race_results_table.find_all('tr')[1:]:  # Skip the header row
    columns = row.find_all('td')
    row_data = [column.text.strip() for column in columns]
    rows.append(row_data)

# Print the extracted data
print(headers)
for row in rows:
    print(row)
# %%


