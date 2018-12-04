import unittest
from datetime import datetime
from icalendar import Event
from bin_collection import print_events_summary_on_given_date, bin_data_to_grouped_dict


def generate_event_on_date(date, summary):
    event = Event()
    event.add('summary', summary)
    event.add('dtstart', date)
    event.add('dtend', date)
    event.add('dtstamp', datetime(2000,1,1,1,1,1))
    return event


class TestBinCollections(unittest.TestCase):

    def test_print_events_summary_on_given_date_NotRaisingAnException_WhenNoEventsAtGivenDate(self):
        try:
            print_events_summary_on_given_date("date",{})
        except:
            self.fail()

    def test_bin_data_to_grouped_dict_ReturnEmptyDict_WhenPassedEmptyList(self):
        event_1 = generate_event_on_date(datetime(2018, 1, 1).date(), 'event_1')
        event_2 = generate_event_on_date(datetime(2018, 1, 1).date(), 'event_2')
        event_3 = generate_event_on_date(datetime(2018, 1, 2).date(), 'event_3')
        event_4 = generate_event_on_date(datetime(2018, 1, 1).date(), 'event_4')
        events = [event_1, event_2, event_3, event_4]

        result = bin_data_to_grouped_dict(events)
        self.assertEqual(len(result.get('20180101')), 3)

    def test_bin_data_to_grouped_dict_GroupEventsCorrectly_WhenPassedUnOrderedEvents(self):
        try:
            print_events_summary_on_given_date("date",{})
        except:
            self.fail()
