## About
A tool which estimates the final fare of a taxi journey within the Cardiff area. 
Using the date and time, the appropriate tariff is determined from those provided by cardiff council found [here](https://www.cardiff.gov.uk/ENG/resident/Parking-roads-and-travel/travel/taxis/taxi-passengers/hackney-carriage/Pages/default.aspx)
The start location and destination are used to find the distance and sections of the journey with an average speed of under 8mph (considered stopped for fare purposes) using the google API.

## Features
- Uses both distance and stopped time to calculate the fare.
- Has options for both immediate and future journeys.
- Factors in extra charges due to day of the week and time.
- Factors in extra charges and a change of fare due to bank holidays and days specified by Cardiff Council.
- Factors in extra charges due to number of passengers.
## How to use
### Acquiring your Google API Key
Due to the use of the Google Maps API, you will require an API key. API keys are generated in the 'Credentials' page of the 'APIs & Services' tab of [Google Cloud console](https://console.cloud.google.com/apis/credentials).
Press the '+ CREATE CREDENTIAL' button to create the key.
Copy the key and paste it into the 'config.py' file.
Do not remove API key access to the 'Directions' and 'Geolocation'.

Finally, run main.py with python 3.10+
