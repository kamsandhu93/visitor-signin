import sys
import urllib.request
import urllib.error
from icalendar import Calendar, Event
from itertools import groupby


def read_bin_data(url):
    """ Reads the icalendar file and return the events,
        Args:
            url(str): the file url
        Returns:
            list(Event): the events
    """

    try:
        response = urllib.request.urlopen(url)
        data = response.read()
        cal = Calendar.from_ical(data)
    except (urllib.error.URLError, urllib.error.HTTPError):
        print('Error downloading the icalendar file')
        sys.exit()
    except Exception as ex:
        print(f'Error reading the icalendar file, message is : {ex}')
        sys.exit()
    return cal.walk(name='VEVENT')


def bin_data_to_grouped_dict(events):
    """ Returns dictionary with keys equal to the date and value is list of events
        Args:
            events(list[Event]): 
        Returns:
            dict: the events grouped by the date
    """
    result = {}
    for event in events:
        key = event.get('DTSTART').to_ical().decode("utf-8")
        result[key] = result.get(key,list())
        result[key].append(event)

    return result


def print_events_summary_on_given_date(date, bin_data):
    if not bin_data.get(date):
        print('No bin collection for the given date, are you sure you have entered the date correctly in YYYYMMMDD format?')
        return
    for event in bin_data.get(date):
        print(event.get('SUMMARY'))


def main(argv):
    bin_data_url = None
    date_requested = None
    try:
        bin_data_url = argv[1]
        date_requested = argv[2]
    except:
        print('Expecting two parameters, the url for the icalendar data file and the date in YYYYMMDD')
        sys.exit()

    bin_data = read_bin_data(bin_data_url)
    grouped_dict = bin_data_to_grouped_dict(bin_data)
    print_events_summary_on_given_date(date_requested, grouped_dict)

if __name__ == "__main__":
    main(sys.argv)
