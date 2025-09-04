#%%
import requests
from bs4 import BeautifulSoup
import boto3
from botocore.exceptions import NoCredentialsError
import json
from datetime import datetime

# Load AWS credentials from the JSON file
with open('/Users/vamseekrishna/Desktop/personal_projects/formula1-aws-etl-pipeline/aws_keys.json', 'r') as f:
    aws_keys = json.load(f)

access_key = aws_keys['access_key']
secret_key = aws_keys['secret_key']
#%%

# URL of the website you want to scrape
url = 'https://www.formula1.com/en/results/2025/races'

# Send a GET request to the website
response = requests.get(url)
print(response.content)
#%%

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Get the HTML content
    html_content = response.content
    
    # Get the current date
    current_date = datetime.now()
    year = current_date.year
    ingested_date = current_date.strftime('%Y-%m-%d')
    
    # AWS S3 bucket details
    bucket_name = 'formula1-aws-etl-data'
    file_name = f'bronze/race_results/{year}/{ingested_date}/raw_html_content.html'
    
    # Initialize a session using Amazon S3 with the provided credentials
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    
    try:
        # Upload the file to S3
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=html_content)
        print(f"File uploaded successfully to {bucket_name}/{file_name}")
    except NoCredentialsError:
        print("Credentials not available")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
# %%

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
