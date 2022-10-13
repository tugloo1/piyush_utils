import json
import pprint
import arrow
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from urllib.parse import parse_qs


def trifit_tennis():
    today = arrow.now().format("MM/DD/YYYY")
    one_week = arrow.now().shift(days=8).format("MM/DD/YYYY")
    response = requests.get('https://www.myiclubonline.com/iclub/scheduling/classSchedule?club=30075&lowDate={0}&highDate={1}&_=1634537506545'.format(today, one_week))
    json_output = json.loads(response.text)
    for event in json_output:
        if event['eventName'] == 'Tennis' and event['enrolled'] == '0':
            keys_to_extract = {'dayOfWeek', 'eventDate', 'eventStartTime', 'eventEndTime', 'locationName'}
            selected = {key: event[key] for key in event if key in keys_to_extract}
            print(selected)


def le_cheviot_hills(selected_date: str, begin_time: str="8:00am"):
    params = {'Action': 'Start', 'date': selected_date, 'begintime': begin_time, 'location': 'Cheviot Hills Pay Tennis', 'keywordoption': 'Match One', 'blockstodisplay': '10', 'frheadcount': '0', 'display': 'Detail', 'module': 'FR'}
    response = requests.get("https://reg.laparks.org/web/wbwsc/webtrac.wsc/search.html", params=params)
    soup_parser = BeautifulSoup(response.content)
    court_htmls = soup_parser.find_all("table", {"id": "frwebsearch_output_table"})
    availability = {}
    for html in court_htmls:
        court_html = html.find("td", {"data-title": "Facility Description"})
        court_name = court_html.text
        availability[court_name] = []
        time_slots = html.find("td", {"class": "cart-blocks"}).find_all("a")
        for slot in time_slots:
            time_slot = slot.text
            if slot.attrs["data-tooltip"] != '<h2>Unavailable</h2>This Facility Reservation time block is unavailable. Please select another time block.':
                availability[court_name].append(time_slot)
            continue
    pprint.pprint(availability)



if __name__ == "__main__":
    # trifit_tennis()
    le_cheviot_hills("09/02/2022")
