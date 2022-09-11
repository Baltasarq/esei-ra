#!/usr/bin/env python
# coding: utf-8
# (c) esei-ra Baltasar 2016/19 MIT License <baltasarq@gmail.com>

from datetime import datetime
from datetime import timedelta

from google.appengine.ext import ndb

from model.classroom import Classroom
from model.subject import Subject
from model.year import Year


class Reserve(ndb.Model):
    WEEK_DAYS = [
        "*",
        "LUN",
        "MAR",
        "MIE",
        "JUE",
        "VIE",
        "SAB",
        "DOM"
    ]

    name = ndb.StringProperty(required=True, indexed=True)
    date_begin = ndb.DateProperty(required=True, indexed=True)
    date_end = ndb.DateProperty(required=True, indexed=True)
    time_begin = ndb.TimeProperty(required=True, indexed=True)
    time_end = ndb.TimeProperty(required=True, indexed=True)
    week_day = ndb.IntegerProperty(default=1, indexed=True)     # isoweekday()
    classroom_key = ndb.KeyProperty(kind=Classroom, indexed=True)
    subject_key = ndb.KeyProperty(kind=Subject, indexed=True)
    notes = ndb.StringProperty(default="")

    def get_classroom(self):
        toret = None
        key = self.classroom_key

        if not key:
            toret = Classroom.get_default()
        else:
            toret = key.get()

        return toret

    def get_subject(self):
        toret = None
        key = self.subject_key

        if not key:
            toret = Subject.get_default()
        else:
            toret = key.get()

        return toret

    def get_day_of_week_as_str(self):
        return Reserve.WEEK_DAYS[self.week_day]

    def get_abbrev_form(self):
        return self.name + ": " + self.get_subject().get_abbrev_form()

    def is_a_match_for_time(self, t):
        if isinstance(t, datetime):
            t = t.time()

        return self.time_begin <= t < self.time_end

    def is_a_match_for_week_day(self, wday):
        return self.week_day == 0 or wday == 0 or self.week_day == wday

    def is_a_match_for_date(self, date):
        if isinstance(date, datetime):
            date = date.date()

        matches_week_day = self.is_a_match_for_week_day(date.isoweekday())
        return matches_week_day and (self.date_begin <= date <= self.date_end)

    @staticmethod
    def retrieve(handler):
        reserve = None
        id = handler.request.GET.get("id")

        if id:
            reserve = ndb.Key(urlsafe=id).get()
            if not reserve:
                handler.redirect("/error?msg=No course for id: " + str(id))
        else:
            handler.redirect("/error?msg=Missing course id.")

        return reserve

    @staticmethod
    def move_all(old_begin_period1,
                 old_end_period1,
                 new_begin_period1,
                 new_end_period1,
                 old_begin_period2,
                 old_end_period2,
                 new_begin_period2,
                 new_end_period2):
        """Moves all reserves in the old period to the new one."""
        all_reserves = Reserve.query().fetch()

        for reserve in all_reserves:
            print("*** Considering reserve:", reserve)

            if (reserve.date_begin == old_begin_period1
            and reserve.date_end == old_end_period1):
                reserve.date_begin = new_begin_period1
                reserve.date_end = new_end_period1
                print("\tModified reserve por period1")
                reserve.put()
            elif (reserve.date_begin == old_begin_period2
              and reserve.date_end == old_end_period2):
                  reserve.date_begin = new_begin_period2
                  reserve.date_end = new_end_period2
                  print("\tModified reserve por period2")
                  reserve.put()

    @staticmethod
    def get_date_of_next_week_day_from(d, wd):
        toret = d
        one_day = timedelta(days=1)

        if wd > 0:
            wd -= 1
            while toret.weekday() != wd:
                toret += one_day

        return toret

    @staticmethod
    def str_from_date(d):
        return str.format("{:04d}-{:02d}-{:02d}", d.year, d.month, d.day)

    @staticmethod
    def build_timetable_info(str_date, str_mode):
        academic_year = Year.retrieve()

        # Date
        today = datetime.today()
        if str_date:
            try:
                today = datetime.strptime(str_date, "%Y-%m-%d")
            except ValueError:
                pass

        # Dates of this week
        date_week_start = today - timedelta(days=today.isoweekday() - 1)

        str_week_dates = [date_week_start.date().isoformat()]
        day = date_week_start
        delta = timedelta(days=1)
        for i in range(1, 7):
            day += delta
            str_week_dates.append(day.date().isoformat())

        # Classrooms
        mode = None
        if str_mode:
            mode = (str_mode == "P")
            classrooms = Classroom.query(Classroom.pract == mode)
        else:
            classrooms = Classroom.query()

        classrooms = classrooms.order(Classroom.name).fetch()

        # Hours
        hour = datetime(2001, 1, 1, academic_year.time_begin.hour, academic_year.time_begin.minute)
        hour_delta = timedelta(minutes=academic_year.time_delta)
        hour_end = datetime(2001, 1, 1, academic_year.time_end.hour, academic_year.time_end.minute)
        hours = [hour]
        hour += hour_delta
        while hour < hour_end:
            hours.append(hour)
            hour += hour_delta

        # Reserves
        queried_reserves = Reserve.query().fetch()
        reserves = {}

        for classroom in classrooms:
            reserves[classroom.key] = []

        for reserve in queried_reserves:
            reserves_per_classroom = reserves.get(reserve.classroom_key)

            if (reserves_per_classroom is not None
            and reserve.is_a_match_for_date(today)):
                reserves_per_classroom.append(reserve)

        # Polish reserves with hours info
        for classroom_key in reserves.keys():
            reserves_per_classroom = reserves[classroom_key]

            # Create new list
            reserves_per_classroom_and_hour = []

            # Populate list honouring hours
            for i, hour in enumerate(hours):
                reserves_per_classroom_and_hour.append([])
                reserves_per_classroom_and_this_hour = reserves_per_classroom_and_hour[-1]

                for reserve in reserves_per_classroom:
                    if reserve.is_a_match_for_time(hour):
                        reserves_per_classroom_and_this_hour.append(reserve)

            reserves[classroom_key] = reserves_per_classroom_and_hour

        del queried_reserves[:]
        return {
            "year": academic_year,
            "today": today,
            "mode": mode,
            "Reserve": Reserve,
            "str_week_dates": str_week_dates,
            "classrooms": classrooms,
            "reserves": reserves,
            "hours": hours,
            "timedelta": timedelta
        }
