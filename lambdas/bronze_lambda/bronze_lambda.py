#%%
import sys
import requests
from bs4 import BeautifulSoup
import boto3
from botocore.exceptions import NoCredentialsError
import json
from datetime import datetime
#%%
def handler(event, context):

    # Load AWS credentials from the JSON file
    with open('aws_keys.json', 'r') as f:
        aws_keys = json.load(f)

    access_key = aws_keys['access_key']
    secret_key = aws_keys['secret_key']
    url = event['url']
    entity = event['entity']

    #url = 'https://www.formula1.com/en/results/2025/races'

# Send a GET request to the website
    response = requests.get(url)
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
        file_name = f'bronze/{entity}/{year}/{ingested_date}/raw_html_content.html'
        
        # Initialize a session using Amazon S3 with the provided credentials
        s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        
        try:
            # Upload the file to S3
            s3.put_object(Bucket=bucket_name, Key=file_name, Body=html_content)
            print(f"File uploaded successfully to {bucket_name}/{file_name}")
            return {'statusCode': 200, 'body': 'File uploaded successfully'}
        except NoCredentialsError:
            print("Credentials not available")
            return {'statusCode': 500, 'body': 'Credentials not available'}
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return {'statusCode': 500, 'body': 'Failed to retrieve the page'}
#%%
#handler(None, None)
# %%
