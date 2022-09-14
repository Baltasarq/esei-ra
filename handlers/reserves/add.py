#!/usr/bin/env python
# esei-ra (c) baltasar 2016 MIT License <baltasarq@gmail.com>

import logging
import webapp2
from datetime import time
from datetime import datetime
from datetime import timedelta

from google.appengine.api import users
from google.appengine.ext import ndb

from model.reserve import Reserve
from model.year import Year
from modify import ModifyReserveHandler


class AddReserveHandler(webapp2.RequestHandler):
    def get(self):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        # Retrieve classroom and hour
        classroom_id = self.request.GET.get("classroom_id")
        str_hour = self.request.GET.get("hour")

        if classroom_id:
            try:
                classroom_key = ndb.Key(urlsafe=classroom_id)
            except:
                classroom_key = None

        if str_hour:
            try:
                hour = datetime.strptime(str_hour, "%H:%M")
            except:
                hour = datetime(2001, 1, 1, 9, 0, 0)

        hour_end = hour + timedelta(hours=1)

        # Retrieve possible begin and end dates
        str_date = self.request.GET.get("date")

        if str_date:
            date_begin = datetime.strptime(str_date, "%Y-%m-%d").date()
            date_end = date_begin + timedelta(days=1)
        else:
            # Determine probable date
            year = Year.retrieve()
            today = datetime.now().date()
            date_begin = today
            date_end = today + timedelta(days=1)

            if (today < year.period1_begin
             or (year.period1_begin < today < year.period1_end)):
                date_begin = year.period1_begin
                date_end = year.period1_end
            else:
                if (today < year.period2_begin
                 or (year.period2_begin < today < year.period2_end)):
                    date_begin = year.period2_begin
                    date_end = year.period2_end

        # Create the new reserve and edit it
        reserve = Reserve(
                    name="Undefined",
                    date_begin=date_begin,
                    date_end=date_end,
                    time_begin=hour.time(),
                    time_end=hour_end.time(),
                    week_day=date_begin.isoweekday(),
                    subject_key=None,
                    classroom_key=classroom_key)

        ModifyReserveHandler.edit_reserve(self, usr, reserve)


app = webapp2.WSGIApplication([
    ('/reserves/add', AddReserveHandler)
], debug=True)
