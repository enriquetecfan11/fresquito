"""
This script scrapes weather data for a given list of locations in Spain and saves it to a CSV file.
It uses the Pelmorex ID of each location to fetch the weather data from the El Tiempo website.
The script also geocodes each location to get its latitude and longitude using the Nominatim API.
The scraped data is saved to a CSV file with the following columns: 'TIPO', 'CIUDAD', 'PROVINCIA', 'GRADOS', 'FECHA', 'HORA UTC', 'HORA MADRID (UTC+2)'.
The script also prints the coldest and hottest towns along with their temperature and creates a map using the Folium library.
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import threading
import datetime
from geopy.geocoders import Nominatim
import folium
import csv
import os
import multiprocessing

# Define the maximum number of parallel threads as half of available CPU cores
MAX_THREADS = multiprocessing.cpu_count() // 2 

# Number of locations to scrape // Max towns in DB 22080
NUM_LOCATIONS = 2000  

# CSV File to save data
csv_filename = 'datos_tiempo.csv'


def geocode_location(town_name, province_name):
    """
    Geocode a given town and province to get its latitude and longitude.
    If geocoding is not successful, return None.
    """
    try:
        location_string = f"{town_name}, {province_name}, Spain"
        locator = Nominatim(user_agent='myGeocoder')
        location = locator.geocode(location_string)
        return (location.latitude, location.longitude)
    except:
        return None


def scrape_weather_data(pelmorex_list):
    total_locations = len(pelmorex_list)
    print(f"Total locations in the database: {total_locations}")
    meteo = []
    threads = []
    for pelmorex_id in pelmorex_list[:NUM_LOCATIONS]: 
        # Print the current name of location being scraped 
        #print(f"Scraping data for location {pelmorex_id} ({pelmorex_list.index(pelmorex_id)+1} of {NUM_LOCATIONS})")

        thread = threading.Thread(target=fetch_weather_data, args=(pelmorex_id, meteo))
        threads.append(thread)
        if len(threads) >= MAX_THREADS:
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            threads = []
            time.sleep(1)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return meteo

def fetch_weather_data(pelmorex_id, meteo):
    """
    Fetch weather data for a given pelmorex_id and append it to the meteo list.
    """
    try:
        url = f'https://www.eltiempo.es/api/v1/get_current_conditions_by_pelmorex_id/{pelmorex_id}'
        response = requests.get(url)
        data = response.json()
        temp_dict = {'pelmorex_id': pelmorex_id, 'temp': data['temperature']['c'], 'timestamp': data['timestamp']['local']}
        meteo.append(temp_dict)
    except:
        pass
    
def save_to_csv(data, filename):
    header = ['TIPO', 'CIUDAD', 'PROVINCIA', 'GRADOS', 'FECHA', 'HORA UTC', 'HORA MADRID (UTC+2)']

    now = datetime.datetime.now()
    date = now.strftime('%d/%m/%Y')
    time_utc = now.strftime('%H:%M:%S')
    time_madrid = (now + datetime.timedelta(hours=2)).strftime('%H:%M:%S')

    formatted_data = {
        'TIPO': data['Type'],
        'CIUDAD': data['Name'],
        'PROVINCIA': data['Province'],
        'GRADOS': data['Temperature'],
        'FECHA': date,
        'HORA UTC': time_utc,
        'HORA MADRID (UTC+2)': time_madrid
    }

    # Add the first row
    if not os.path.exists(filename):
        with open('meteorologia.csv','w+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()
            # Append new rows
            writer.writerow(formatted_data)
    else:
        # Append new rows
        with open('meteorologia.csv','a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writerow(formatted_data)

    # Check if the CSV file already exists
    file_exists = os.path.exists(filename)

    # Write data to CSV file
    with open(filename, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        if not file_exists:
            writer.writeheader()
        writer.writerow(formatted_data)

def main():
    global NUM_LOCATIONS  # Indicate that you are using the global variable
    print('Main function running...')
    print(f"CPU Count:", multiprocessing.cpu_count())
    print(f"Running with {MAX_THREADS} threads...")

    try:
        # Start Time Script
        start_time = datetime.datetime.now()
        now = datetime.datetime.now()
        print('Process started on', str(now.day)+'-'+str(now.month)+'-'+str(now.year), 'at', str(now.hour)+':'+str(now.minute))
        
        # Load town_index
        town_index = pd.read_csv('town_index.csv')

        # Scrape weather data
        pelmorex_list = town_index['pelmorex_id'].tolist()
        meteo_data = scrape_weather_data(pelmorex_list[:NUM_LOCATIONS])  # Limit to user-specified number
        meteo_df = pd.DataFrame(meteo_data)

        # Merge dataframes
        output = pd.merge(town_index, meteo_df, on='pelmorex_id', how='left')
        output.to_csv('output.csv', index=False)

        # Get coldest and hottest towns
        coldest = output[output['temp'] == output['temp'].min()].sample()
        hottest = output[output['temp'] == output['temp'].max()].sample()

        # Print coldest and hottest towns
        print("Coldest Town:")
        print(f"Name: {coldest['name'].iloc[0]}, Province: {coldest['province'].iloc[0]}, Temperature: {coldest['temp'].iloc[0]}ºC")
        print("Hottest Town:")
        print(f"Name: {hottest['name'].iloc[0]}, Province: {hottest['province'].iloc[0]}, Temperature: {hottest['temp'].iloc[0]}ºC")

        # Create map
        temp_map = folium.Map()

        # Geocode coldest and hottest towns
        c_coords = geocode_location(coldest['name'].iloc[0], coldest['province'].iloc[0])
        h_coords = geocode_location(hottest['name'].iloc[0], hottest['province'].iloc[0])

        # Save hottest and coldest towns to CSV
        
        hottest_data = {
        'Type': 'Hottest',
        'Name': hottest['name'].iloc[0],
        'Province': hottest['province'].iloc[0],
        'Temperature': hottest['temp'].iloc[0]
        }

        coldest_data = {
        'Type': 'Coldest',
        'Name': coldest['name'].iloc[0],
        'Province': coldest['province'].iloc[0],
        'Temperature': coldest['temp'].iloc[0]
        }

        save_to_csv(hottest_data, csv_filename)
        save_to_csv(coldest_data, csv_filename)


        if c_coords and h_coords:
            folium.Marker(location=c_coords,
                          popup=f"{coldest['name'].iloc[0]}, {coldest['province'].iloc[0]}\n{coldest['temp'].iloc[0]}ºC",
                          icon=folium.Icon(color='blue', icon='glyphicon glyphicon-cloud')
                          ).add_to(temp_map)

            folium.Marker(location=h_coords,
                          popup=f"{hottest['name'].iloc[0]}, {hottest['province'].iloc[0]}\n{hottest['temp'].iloc[0]}ºC",
                          icon=folium.Icon(color='red', icon='glyphicon glyphicon-fire')
                          ).add_to(temp_map)

            temp_map.fit_bounds([c_coords, h_coords])

            # Save the map
            temp_map.save(outfile="index.nginx-debian.html")
            temp_map.save('map.html')

            now = datetime.datetime.now()
            print('Map generated successfully on', str(now.day)+'-'+str(now.month)+'-'+str(now.year), 'at', str(now.hour)+':'+str(now.minute))

            # Stop time script
            now = datetime.datetime.now()
            print('Process finished on', str(now.day)+'-'+str(now.month)+'-'+str(now.year), 'at', str(now.hour)+':'+str(now.minute))
            
            # Script execution time
            print('Script execution time:', str(now - start_time))
            print('\n')

        else:
            print('Geocoding failed for coldest or hottest town.')
    except Exception as e:
        now = datetime.datetime.now()
        print('Process FAILED on', str(now.day)+'-'+str(now.month)+'-'+str(now.year), 'at', str(now.hour)+':'+str(now.minute))
        print(f'Error: {str(e)}')
        print('\n')

if __name__ == "__main__":
    main()
