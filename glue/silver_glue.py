#%%
import boto3
import pandas as pd
from bs4 import BeautifulSoup

# AWS S3 bucket details
source_bucket_name = 'formula1-aws-etl-data'
source_file_key = 'bronze/race_results/2025/2025-09-02/raw_html_content.html'
destination_bucket_name = 'formula1-aws-etl-data'
destination_file_key = 'silver/race_results/2025-09-01/race_results.csv'

# Initialize a session using Amazon S3
s3 = boto3.client('s3')

print("Starting AWS Glue job...")

try:
    # Download the HTML file from S3
    print(f"Downloading HTML file from {source_bucket_name}/{source_file_key}")
    html_obj = s3.get_object(Bucket=source_bucket_name, Key=source_file_key)
    html_content = html_obj['Body'].read()
    print("HTML file downloaded successfully.")
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    print("HTML content parsed successfully.")
    
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
    print("Race details extracted successfully.")
    
    # Create a DataFrame from the extracted race results
    df_race_results = pd.DataFrame(race_results)
    print("DataFrame created successfully.")
    
    # Convert DataFrame to CSV
    csv_buffer = df_race_results.to_csv(index=False)
    print("DataFrame converted to CSV successfully.")
    
    # Upload the CSV to the destination S3 bucket
    s3.put_object(Bucket=destination_bucket_name, Key=destination_file_key, Body=csv_buffer)
    print(f"DataFrame uploaded successfully to {destination_bucket_name}/{destination_file_key}")

except Exception as e:
    print(f"An error occurred: {e}")

print("AWS Glue job completed.")

# %%
