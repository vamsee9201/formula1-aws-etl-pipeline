#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website you want to scrape
url = 'https://www.formula1.com/en/results/2025/races'

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract race details from the HTML content
    race_results = []
    for row in soup.select('table tbody tr'):
        columns = row.find_all('td')
        if len(columns) > 0:
            grand_prix = columns[0].text.strip()
            date = columns[1].text.strip()
            winner = columns[2].text.strip()
            team = columns[3].text.strip()
            laps = columns[4].text.strip()
            time = columns[5].text.strip()
            race_results.append({
                'Grand Prix': grand_prix,
                'Date': date,
                'Winner': winner,
                'Team': team,
                'Laps': laps,
                'Time': time
            })
    
    # Print extracted race results
    for result in race_results:
        print(result)

    # Create a DataFrame from the extracted race results
    df_race_results = pd.DataFrame(race_results)

    # Display the DataFrame
    print(df_race_results)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

# %%
