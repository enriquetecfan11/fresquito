import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import threading
import datetime
from geopy.geocoders import Nominatim
import folium

MAX_THREADS = 4  # Define the maximum number of parallel threads
# NUM_LOCATIONS = 100  # Number of locations to scrape // Max towns in DB 22080

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
        print(f"Scraping data for location {pelmorex_id} ({pelmorex_list.index(pelmorex_id)+1} of {NUM_LOCATIONS})")

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

def main():
    global NUM_LOCATIONS  # Indicate that you are using the global variable
    print('Main function running...')
    
    
    try:
        # Load town_index
        town_index = pd.read_csv('town_index.csv')

        # Get user input for the number of locations to scrape
        user_input = input("Enter the number of locations to scrape: ")
        NUM_LOCATIONS = int(user_input)

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
            temp_map.save(outfile="index.nginx-debian.html")

            now = datetime.datetime.now()
            print('Map generated successfully on', str(now.day)+'-'+str(now.month)+'-'+str(now.year), 'at', str(now.hour)+':'+str(now.minute))
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
