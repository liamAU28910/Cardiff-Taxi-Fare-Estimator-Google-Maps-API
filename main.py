import config
import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key=config.api_key)


def get_user_inputs():
    """
    Prompts the user to provide the information required to calculate their taxi fare.
    They are prompted for the: start location; destination; time of travel; number of passengers;
    and quantity of luggage.
    :return:
        str: The starting location.
        str: The destination.
        datetime: The date and time of departure.
        int: The number of passengers travelling.
        int: The number of large luggage items accompanying the passengers.
    """
    gc = []
    while not gc:
        start_location = str(input("Please input your starting location: "))
        gc = gmaps.geocode(start_location)  # Find the geocode of the given location
        if not gc:  # If the geocode is empty, the location cannot be found and must be re-inputted.
            print("Location not found. Please be more specific and try again.")
    gc = []
    while not gc:
        end_location = str(input("Please input your destination: "))
        gc = gmaps.geocode(end_location)
        if not gc:
            print("Location not found. Please be more specific and try again.")

    valid_input_1 = False
    while not valid_input_1:
        is_now_input = str(input("Do you wish to travel now? (Y/n): "))
        match is_now_input.lower():
            case '':
                is_now = True
                valid_input_1 = True
            case 'y':
                is_now = True
                valid_input_1 = True
            case 'yes':
                is_now = True
                valid_input_1 = True
            case 'n':
                is_now = False
                valid_input_1 = True
            case 'no':
                is_now = False
                valid_input_1 = True
            case _:
                valid_input_1 = False

    if not is_now:
        valid_input_2 = False
        while not valid_input_2:
            dt_str = str(input("Input the date and time of departure (dd/mm/yy hh:mm) : "))
            try:
                departure_datetime = datetime.strptime(dt_str, '%d/%m/%y %H:%M')
                valid_input_2 = True
            except Exception as e:
                print(e)
                valid_input_2 = False
                print("Please try again. Check that the format is correct.")
    if is_now:
        departure_datetime = datetime.now()

    valid_input_3 = False
    while not valid_input_3:
        try:
            passenger_num = int(input("Input the number of passengers : "))
            valid_input_3 = True
        except Exception as e:
            print(e)
            valid_input_3 = False
            print("Please try again.")

    valid_input_4 = False
    while not valid_input_4:
        try:
            large_items_num = int(
                input("Input the number of Bicycles, Cabin Trunks and items of furniture you are bringing : "))
            valid_input_4 = True
        except Exception as e:
            print(e)
            valid_input_4 = False
            print("Please try again.")

    return start_location, end_location, departure_datetime, passenger_num, large_items_num
