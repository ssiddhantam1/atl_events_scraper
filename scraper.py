import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

url = 'https://discoveratlanta.com/events/all/'

# Set up Chrome options
chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode to avoid opening a new window

# Create a Chrome service
chrome_service = ChromeService()

# Create a Chrome WebDriver instance
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Fetch the webpage content
response = requests.get(url)

if response.status_code == 200:
    webpage = response.content
    soup = BeautifulSoup(webpage, 'html.parser')

    # Extract event details
    events = soup.find_all('article', class_='listing')
    event_list = []
    count=0
    for event in events:
        title_element = event.find('h4', class_='listing-title')

        if title_element:
            title = title_element.text.strip()
            link = title_element.find('a')['href']
            event_url = link

            # Visit the event link
            driver.get(event_url)
            time.sleep(2)  # Allow time for the event page to load

            # Get the page source after waiting
            event_page_source = driver.page_source

            # Use BeautifulSoup to parse the event page HTML
            event_soup = BeautifulSoup(event_page_source, 'html.parser')

            # Extract event details (modify this part based on your HTML structure)
            date_element = event_soup.find('strong', string='Date(s):')
            date = date_element.find_next('td').text.strip() if date_element else ''

            start_time_element = event_soup.find('strong', string='Start time:')
            start_time = start_time_element.find_next('td').text.strip() if start_time_element else ''

            end_time_element = event_soup.find('strong', string='End time:')
            end_time = end_time_element.find_next('td').text.strip() if end_time_element else ''

            location_element = event_soup.find('strong', string='Location:')
            location = location_element.find_next('td', class_='event-address').text.strip() if location_element else ''

            type_element = event_soup.find('strong', string='Type:')
            event_type = type_element.find_next('td').text.strip() if type_element else ''

            # Append event details to the list
            event_list.append({
                'Title': title,
                'Link': link,
                'Date': date,
                'Start Time': start_time,
                'End Time': end_time,
                'Location': location,
                'Event Type': event_type
            })

            count+=1
            
            print("event feteched : {}".format(count))

    # Create a DataFrame from the list of events
    df = pd.DataFrame(event_list)

    # Save to a CSV file
    df.to_csv('eventsdetails.csv', index=False)
    print('Data successfully scraped and saved to eventsdetails.csv.')
else:
    print('Failed to fetch the webpage.')
