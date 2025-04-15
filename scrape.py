import pandas as pd
import requests
from bs4 import BeautifulSoup
import schedule
import time
import streamlit as st

# Example scraping function
def scrape_website():
    url = 'https://olx.ba/pretraga?attr=&attr_encoded=1&category_id=2&page=1&sort_by=date&sort_order=desc'  # Replace with your target URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the data you need (define your fields here)
    data = {
        "Field 1": soup.find('tag1').text,  # Replace 'tag1' with the actual HTML tag
        "Field 2": soup.find('tag2').text,
        "Timestamp": pd.Timestamp.now()  # To track when the data is scraped
    }
    return data

# Function to check and update data
def update_data():
    global df
    new_data = scrape_website()

    # Convert new_data to DataFrame for easy comparison
    new_data_df = pd.DataFrame([new_data])

    # Check for duplicates - you can customize this further
    is_duplicate = df[["Field 1", "Field 2"]].isin(new_data_df[["Field 1", "Field 2"]].iloc[0]).all(axis=1).any()

    if not is_duplicate:
        # Append only if it's not a duplicate
        df = pd.concat([df, new_data_df], ignore_index=True)
        df.to_csv("scraped_data.csv", index=False)
        print("New data added!")
    else:
        print("Duplicate data. Nothing added!")

# Initialize DataFrame from saved file
try:
    df = pd.read_csv("scraped_data.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Field 1", "Field 2", "Timestamp"])  # Initialize an empty dataframe

# Streamlit UI
st.title("Daily Scraper with Duplicate Check")
if st.button("Scrape Now"):
    update_data()
    st.write("Scraping completed. Check below for updates.")
    
st.dataframe(df)

# Schedule Automated Scraping
schedule.every().day.at("10:00").do(update_data)  # Change schedule as required

# Keep the script running for scheduling
while True:
    schedule.run_pending()
    time.sleep(1)
