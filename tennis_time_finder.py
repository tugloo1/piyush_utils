import json
import arrow
from bs4 import BeautifulSoup
import requests


class Locations:
    cheviot_hills = "Cheviot Hills Pay Tennis"
    vermont_canyon = "Vermont Canyon Pay Tennis"
    westwood = "Westwood Pay Tennis"
    stoner = "Stoner RC"

today = arrow.now()
one_week = arrow.now().shift(days=8)


def trifit_tennis():
    today_format = today.format("MM/DD/YYYY")
    one_week_format = one_week.format("MM/DD/YYYY")
    response = requests.get('https://www.myiclubonline.com/iclub/scheduling/classSchedule?club=30075&lowDate={0}&highDate={1}&_=1634537506545'.format(today_format, one_week_format))
    json_output = json.loads(response.text)
    for event in json_output:
        if event['eventName'] == 'Tennis' and event['enrolled'] == '0':
            keys_to_extract = {'dayOfWeek', 'eventDate', 'eventStartTime', 'eventEndTime', 'locationName'}
            selected = {key: event[key] for key in event if key in keys_to_extract}
            print(selected)


def la_tennis_parks_court_finder(selected_date: str, begin_time: str, location: str):
    params = {'Action': 'Start',
              'date': selected_date,
              'begintime': begin_time,
              'location': location,
              'keywordoption': 'Match One',
              'blockstodisplay': '10',
              'frheadcount': '0',
              'display': 'Detail',
              'module': 'FR'}
    exclusion_criteria = {
        '<h2>Unavailable</h2>This Facility Reservation time block is unavailable. Please select another time block.',
        '<h2>Unavailable</h2>The begin date and time have already passed.'
    }

    response = requests.get("https://reg.laparks.org/web/wbwsc/webtrac.wsc/search.html", params=params)
    soup_parser = BeautifulSoup(response.content, features="html.parser")
    court_htmls = soup_parser.find_all("table", {"id": "frwebsearch_output_table"})
    availability = {}
    for html in court_htmls:
        court_html = html.find("td", {"data-title": "Facility Description"})
        court_name = court_html.text
        availability[court_name] = []
        time_slots = html.find("td", {"class": "cart-blocks"}).find_all("a")
        for slot in time_slots:
            time_slot = slot.text.lstrip()
            start_time = arrow.get(time_slot.split('-')[0].rstrip(), 'h:mm a')
            if slot.attrs["data-tooltip"] not in exclusion_criteria:
                availability[court_name].append(start_time)
            continue
    return availability


def print_out_court_availability(selected_date: str, location: str, begin_time: str = "8:00 am"):
    print("Court Availability for {0} on {1}".format(location, selected_date))
    availability = la_tennis_parks_court_finder(selected_date, begin_time=begin_time, location=location)
    # pprint.pprint(availability)
    court_availability_dict = {}
    for court, times in availability.items():
        for time in times:
            if time not in court_availability_dict:
                court_availability_dict[time] = [court]
            else:
                court_availability_dict[time].append(court)
    for start_time in sorted(court_availability_dict.keys()):
        print("{0} -> {1}".format(start_time.format("h:mm a"), str(court_availability_dict[start_time])))

def print_out_availability_for_next_week(location: str):
    current_date = today
    while current_date < one_week:
        print_out_court_availability(current_date.format("MM/DD/YYYY"), location)
        print("\n")
        current_date = current_date.shift(days=1)
    pass


def check_all_courts_for_date_and_time(selected_date: str, begin_time: str):
    for location in {Locations.cheviot_hills, Locations.stoner, Locations.westwood}:
        print_out_court_availability(selected_date, location=location, begin_time=begin_time)



if __name__ == "__main__":
    # trifit_tennis()
    # print_out_availability_for_next_week(Locations.cheviot_hills)
    check_all_courts_for_date_and_time("05/12/2023", "5:00 pm")
    # print_out_court_availability("05/12/2023", location=Locations.westwood)

