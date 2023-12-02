import datetime
import re
import time
from datetime import datetime


class DateParser(object):
    """
    A class to represent date parser.

    ...

    Attributes
    ----------
    _instance : DateParser
        an instance of date parser

    Methods
    -------
    parse_date(dates)
        Parses date assuming the dates come from turkishnetworktimes.
    parse_month(dates)
        Parses month from given date list.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def parse_date(self, dates):
        # Remove Yayınlanma: and Güncelleme: from start of the dates[0] and dates[5]
        dates[0] = dates[0][11:]
        dates[5] = dates[5][11:]
        dates[1],dates[6] = self.parse_month(dates)
        dates[0],dates[5] = self.format_dates(dates)
        publish_date = f"{dates[2]}-{dates[1]}-{dates[0]}"
        update_date = f"{dates[7]}-{dates[6]}-{dates[5]}"

        return publish_date, update_date

    
    def parse_month(self,dates):
        months = {'Ocak': '01', 'Şubat': '02', 'Mart': '03', 'Nisan': '04', 'Mayıs': '05', 'Haziran': '06',
                  'Temmuz': '07', 'Ağustos': '08', 'Eylül': '09', 'Ekim': '10', 'Kasım': '11', 'Aralık': '12'}
        return months[dates[1]], months[dates[6]]



    def format_dates(self,dates):
        date_first = dates[0]
        date_second = dates[5]
        if int(date_first) < 10:
            date_first = f"0{dates[0]}"
        if int(date_second) < 10:
            date_second = f"0{dates[5]}"
        return date_first, date_second