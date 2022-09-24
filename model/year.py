#!/usr/bin/env python
# (c) esei-ra Baltasar 2016/19 MIT License <baltasarq@gmail.com>


import time
from datetime import datetime

from google.appengine.ext import ndb


class Year(ndb.Model):
    name = ndb.StringProperty(required=True)
    period_name = ndb.StringProperty(default="cuatrimestre")
    period1_begin = ndb.DateProperty(required=True)
    period1_end = ndb.DateProperty(required=True)
    period2_begin = ndb.DateProperty(required=True)
    period2_end = ndb.DateProperty(required=True)
    time_begin = ndb.TimeProperty() 				# for example, 9:00
    time_end = ndb.TimeProperty()                   # for example, 21:00
    time_delta = ndb.IntegerProperty(default=30)    # duration for each timetable's cell
    
    def is_within_periods(d: datetime) -> int:
        """Determines wether a given date falls within period 1, period 2, or None.

           :param d: The date to evaluate as falling in this year or not.
           :return: -1 no period, 1 period 1, 2 period 2.
        """
        toret = -1
        
        if ( d >= self.period1_begin
         and d <= self.period1_end):
            toret = 1
        elif ( d >= self.period2_begin
         and d <= self.period2_end):
            toret = 2
         
        return toret

    @staticmethod
    def create(d: datetime) -> Year:
        """Creates a Year appropiate for the given date, and stores it."""
        str_current_year = str.format("{:04d}", d.year)
        str_next_year = str.format("{:04d}", d.year + 1)
        name = str_current_year + "/" + str_next_year[-2:]
        year = Year(
            name=name,
            period_name="cuatrimestre",
            period1_begin=datetime(d.year, 9, 7),
            period1_end=datetime(d.year + 1, 1, 30),
            period2_begin=datetime(d.year + 1, 2, 1),
            period2_end=datetime(d.year + 1, 5, 15),
            time_begin=datetime(d.year, d.month, dent.day, 9, 0).time(),
            time_end=datetime(d.year, d.month, d.day, 21, 0).time(),
            time_delta=30)

        toret = year.put()
        time.sleep(1)
        return toret

    @staticmethod
    def retrieve(d: datetime) -> Year:
        """Looks in the data store for the more appropriate year, given a date.
        
            :param d: The date to find a Year for.
            :return: A Year that contains the given date.
        """
        toret = None
        years = Year.query().order(-self.period1_begin)

        for year in years:
            if year.is_within_periods(d) > 0:
                toret = year
                
        if not toret:
            toret = Year.create(d).get()
            
        return toret
