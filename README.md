# Taxi-Price-Estimator-Google-Maps-API
## About
Outdated. Uses fare data from 2020. Not compatible with updated fare rates due to new fares using wait-time instead of time generally. You would need to know time spend under 8mph to calculate the new fares which cannot easily be established from google directions.
A text-based tool which estimates the final fare of a taxi journey within the Cardiff area. 
## Features
- Uses both distance and time to calculate the fare.
- Has options for both immediate and future journeys.
- Factors in extra charges due to day of the week and time.
- Factors in extra charges due to number of passengers and luggage.
## How to use
### Acquiring your Google API Key
Due to the use of the Google Maps API, you will require an API key. API keys are generated in the 'Credentials' page of the 'APIs & Services' tab of [Google Cloud console](https://console.cloud.google.com/apis/credentials).
Press the '+ CREATE CREDENTIAL' button to create the key.
Copy the key and paste it into the 'config.py' file.
Do not remove API key access to the 'Directions' and 'Geolocation'.

Finally, run main.py with python 3.10+
