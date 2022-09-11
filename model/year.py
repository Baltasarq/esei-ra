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

    @staticmethod
    def create():
        current = datetime.today()
        str_current_year = str.format("{:04d}", current.year)
        str_next_year = str.format("{:04d}", current.year + 1)
        name = str_current_year + "/" + str_next_year[-2:]
        year = Year(
            name=name,
            period_name="cuatrimestre",
            period1_begin=datetime(current.year, 9, 7),
            period1_end=datetime(current.year + 1, 1, 30),
            period2_begin=datetime(current.year + 1, 2, 1),
            period2_end=datetime(current.year + 1, 5, 15),
            time_begin=datetime(current.year, current.month, current.day, 9, 0).time(),
            time_end=datetime(current.year, current.month, current.day, 21, 0).time(),
            time_delta=30)

        toret = year.put()
        time.sleep(1)
        return toret

    @staticmethod
    def retrieve():
        years = Year.query()

        if years.count() == 0:
            toret = Year.create().get()
        else:
            toret = years.get()

        return toret
