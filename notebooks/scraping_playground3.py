#%%
import requests
from bs4 import BeautifulSoup

# List of URLs to fetch
urls = [
    'https://www.formula1.com/en/results/2025/races',
    'https://www.formula1.com/en/results/2025/drivers',
    'https://www.formula1.com/en/results/2025/team'
]

# Function to fetch and save HTML content
for url in urls:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Create a filename based on the URL
        filename = url.split('/')[-1] + '.html'
        # Update filenames to be specific
        if 'races' in url:
            filename = 'races.html'
        elif 'drivers' in url:
            filename = 'drivers.html'
        elif 'team' in url:
            filename = 'teams.html'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())
        print(f"Saved HTML content from {url} to {filename}")
    else:
        print(f"Failed to fetch {url}, status code: {response.status_code}")
#%%
