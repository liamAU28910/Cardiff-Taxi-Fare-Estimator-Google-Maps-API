import config
import googlemaps
from datetime import datetime, time
from govuk_bank_holidays.bank_holidays import BankHolidays


gmaps = googlemaps.Client(key=config.api_key)


def get_user_inputs():
    """
    Prompts the user to provide the information required to calculate their taxi fare.
    They are prompted for the: start location; destination; time of travel; and number of passengers.
    :return: Implied tuple of: The starting location, destination, datetime of departure and the number of passengers travelling.
    :rtype: (str, str, datetime, int)
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

    return start_location, end_location, departure_datetime, passenger_num


def price_calculation(start_location, end_location, departure_datetime, passenger_num, base_rate,
                      base_dist, add_dist, add_rate, time_per_charge, time_rate, extra_passenger_rate,
                      free_passenger_num):
    """
    Calculates and returns the total cost of the journey.
    :param start_location: The starting/pickup location of the journey.
    :type start_location: str
    :param end_location: The location of the destination of the journey.
    :type end_location: str
    :param departure_datetime: The date and time of the taxi's departure.
    :type departure_datetime: datetime
    :param passenger_num: The number of passengers travelling in the taxi. Does not include the driver.
    :type passenger_num: int
    :param base_rate: The base rate for the minimum distance
    :type base_rate: float
    :param base_dist: The minimum distance in metres
    :type base_dist: float
    :param add_dist: The distance between each additional distance-charge.
    :type add_dist: float
    :param add_rate: The rate per additional distance-charge.
    :type add_rate: float
    :param time_per_charge: The time between each time-charge in seconds.
    :type time_per_charge: int
    :param time_rate: The rate per time-charge in seconds.
    :type time_rate: float
    :param free_passenger_num: The number of passenger who do not result in an additional charge.
    :type free_passenger_num: int
    :param extra_passenger_rate: The additional charge per passenger over the free passenger limit.
    :type extra_passenger_rate: float
    :return: The estimated total cost of the journey (£.p) and the estimated journey time (seconds).
    :rtype: (float, int)
    """

    directions_result = gmaps.directions(start_location, end_location, departure_time=departure_datetime)
    distance = directions_result[0]['legs'][0]['distance']['value']
    time_taken = directions_result[0]['legs'][0]['duration']['value']
    time_under_8_mph = 0
    for step in directions_result[0]['legs'][0]['steps']:
        if (step['distance']['value']/step['duration']['value']) < 3.57632:
            time_under_8_mph += step['duration']['value']

    # Price for distance:
    if distance > base_dist:
        distance_price = ((distance - base_dist) / add_dist) * add_rate + base_rate
    else:
        distance_price = base_rate
    # Price for time:
    time_price = (time_under_8_mph / time_per_charge) * time_rate
    # Price for extras:
    extra_price = 0
    if passenger_num > free_passenger_num:
        extra_price += (passenger_num - free_passenger_num) * extra_passenger_rate
    daymonth = (departure_datetime.day, departure_datetime.month)
    extra_fare_days = [(1, 1), (24, 12), (25, 12), (26, 12), (31, 12)]
    if daymonth in extra_fare_days:
        extra_price += 3

    total = round((distance_price + time_price + extra_price), 2)
    print("Distance Cost: £" + str(round(distance_price, 2)))
    print("Stopped Time Cost: £" + str(round(time_price, 2)))
    print("Extra Charges: £" + str(round(float(extra_price), 2)))

    return total, time_taken


def choose_tariff(start_location, end_location, departure_datetime, passenger_num):
    """
    Chooses the appropriate tariff for the departure time and returns total price and journey time.
    :param start_location:
    :type: str
    :param end_location:
    :type: str
    :param departure_datetime:
    :type: datetime
    :param passenger_num:
    :type: int
    :return: The total cost of the journey and the estimated journey time.
    :rtype: (float, int)
    """
    def tariff_1(sl, el, dep_dt, pass_num):
        return price_calculation(sl, el, dep_dt, pass_num,
        3.5, 228.6, 155.88, 0.2, 40, 0.3, 1, 4)

    def tariff_2(sl, el, dep_dt, pass_num):
        return price_calculation(sl, el, dep_dt, pass_num,
        3.5, 228.6, 137.16, 0.2, 35, 0.3, 1, 4)

    def tariff_3(sl, el, dep_dt, pass_num):
        return price_calculation(sl, el, dep_dt, pass_num,
        3.5, 228.6, 118.87, 0.2, 30, 0.3, 1, 4)

    weekday = departure_datetime.weekday()
    start_time = departure_datetime.time()
    bank_holidays = BankHolidays()  # Uses UK Government Bank Holiday API library to get list of all bank holidays in the next few years.
    bank_holiday_date_list = []
    for bank_holiday in bank_holidays.get_holidays():
        bank_holiday_date_list.append(bank_holiday['date'])

    if departure_datetime.date() in bank_holiday_date_list:  # If it is a bank holiday:
        print("Tariff 3")
        total_price, journey_time = tariff_3(start_location, end_location, departure_datetime, passenger_num)
    elif 0 <= weekday < 5 and time(5) < start_time < time(20):  # If it is between 5am and 8pm on a weekday:
        print("Tariff 1")
        total_price, journey_time = tariff_1(start_location, end_location, departure_datetime, passenger_num)
    elif (0 <= weekday < 5 and time(20) < start_time < time(22)) or (weekday >= 5 and time(5) < start_time < time(20)):  # If it is between 5am and 8pm on a weekend or 8am and 10pm on a weekday.
        print("Tariff 2")
        total_price, journey_time = tariff_2(start_location, end_location, departure_datetime, passenger_num)
    else:  # All else (between 10pm and 5am on a weekday. Between 8pm and 5am on a weekend.)
        total_price, journey_time = tariff_3(start_location, end_location, departure_datetime, passenger_num)

    return total_price, journey_time

def main():
    start_location, end_location, departure_datetime, passenger_num = get_user_inputs()

    total_price, journey_time = choose_tariff(start_location, end_location, departure_datetime, passenger_num)

    print("\nYour journey should take ", int(journey_time / 60), " Minutes.")
    print("Your total fare should be: £", total_price)

if __name__ == '__main__':
    main()
