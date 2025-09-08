#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of URLs to fetch
urls = [
    'https://www.formula1.com/en/results/2025/races',
    'https://www.formula1.com/en/results/2025/drivers',
    'https://www.formula1.com/en/results/2025/team'
]

# Initialize variables to store HTML content
races_html = None
drivers_html = None
teams_html = None

def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"Failed to fetch {url}, status code: {response.status_code}")
        return None

# Use the function to fetch HTML content
races_html = fetch_html('https://www.formula1.com/en/results/2025/races')
drivers_html = fetch_html('https://www.formula1.com/en/results/2025/drivers')
teams_html = fetch_html('https://www.formula1.com/en/results/2025/team')

#%%
print(races_html)
#%%
print(drivers_html)
print(teams_html)
# %%

def extract_race_details(soup):
    race_results = []
    for row in soup.select('table tbody tr'):
        columns = row.find_all('td')
        if len(columns) > 0:
            grand_prix = columns[0].text.strip()
            date = columns[1].text.strip()
            winner_span = columns[2].find('span', class_='hide-for-tablet')
            winner = winner_span.text.strip() if winner_span else columns[2].text.strip()
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
    return pd.DataFrame(race_results)


def extract_driver_details(soup):
    driver_results = []
    for row in soup.select('table tbody tr'):
        columns = row.find_all('td')
        if len(columns) > 0:
            position = columns[0].text.strip()
            driver_name = columns[1].text.strip()
            nationality = columns[2].text.strip()
            team = columns[3].text.strip()
            points = columns[4].text.strip()
            driver_results.append({
                'Position': position,
                'Driver': driver_name,
                'Nationality': nationality,
                'Team': team,
                'Points': points
            })
    return pd.DataFrame(driver_results)


def extract_team_standings(soup):
    team_standings = []
    for row in soup.select('table tbody tr'):
        columns = row.find_all('td')
        if len(columns) > 0:
            position = columns[0].text.strip()
            team_name = columns[1].text.strip()
            points = columns[2].text.strip()
            team_standings.append({
                'Position': position,
                'Team': team_name,
                'Points': points
            })
    return pd.DataFrame(team_standings)
#%%
# Use the functions to extract data
if races_html:
    df_race_results = extract_race_details(races_html)
    print(df_race_results)
#%%

if drivers_html:
    df_driver_results = extract_driver_details(drivers_html)
    print(df_driver_results)
#%%

if teams_html:
    df_team_standings = extract_team_standings(teams_html)
    print(df_team_standings)

# %%
