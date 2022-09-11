#!/usr/bin/env python
# coding: utf-8
# esei-ra (c) baltasar 2016 MIT License <baltasarq@gmail.com>


import time
from datetime import datetime
import logging
import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

from model.appinfo import AppInfo
from model.year import Year
from model.reserve import Reserve


class YearManagementHandler(webapp2.RequestHandler):
    def get(self):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        # Retrieve year
        year = Year.retrieve()

        # Render year
        try:
            template_values = {
                "usr": usr,
                "users": users,
                "info": AppInfo,
                "year": year
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("edit_year.html", **template_values))
        except Exception as e:
            logging.error("editing year", str(e))
            self.response.write("ERROR: " + str(e))

    def post(self):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        try:
            # Get the data
            str_move_existing_entries = self.request.get("chkMoveExistingReserves", "")
            name = self.request.get("edName", "").strip().upper()
            period_name = self.request.get("edPeriodName", "2000/01").strip().title()
            str_period1_begin = self.request.get("edPeriod1Begin", "2000-09-07").strip()
            str_period1_end = self.request.get("edPeriod1End", "20001-01-31").strip()
            str_period2_begin = self.request.get("edPeriod2Begin", "2001-02-01").strip()
            str_period2_end = self.request.get("edPeriod2End", "20001-05-15").strip()
            str_time_begin = self.request.get("edTimeBegin", "09:00:00").strip()
            str_time_end = self.request.get("edTimeEnd", "21:00:00").strip()
            str_time_delta = self.request.get("edTimeDelta", "30").strip()

            # Move reserves?
            move_existing_entries = (str_move_existing_entries == "on")

            # Verify
            if not name:
                return self.redirect("/error?msg=Falta nombre para el año.")

            if not period_name:
                return self.redirect("/error?msg=Falta el nombre del período para el año.")

            try:
                period1_begin = datetime.strptime(str_period1_begin, "%Y-%m-%d")
            except ValueError:
                return self.redirect("/error?msg=Comienzo periodo 1 incorrecto para el año.")

            try:
                period1_end = datetime.strptime(str_period1_end, "%Y-%m-%d")
            except ValueError:
                return self.redirect("/error?msg=Fin periodo 1 incorrecto para el año.")

            try:
                period2_begin = datetime.strptime(str_period2_begin, "%Y-%m-%d")
            except ValueError:
                return self.redirect("/error?msg=Comienzo periodo 2 incorrecto para el año.")

            try:
                period2_end = datetime.strptime(str_period2_end, "%Y-%m-%d")
            except ValueError:
                return self.redirect("/error?msg=Fin periodo 2 incorrecto para el año.")

            try:
                if len(str_time_begin) < 8:
                    str_time_begin += ":00"

                time_begin = datetime.strptime(str_time_begin, "%H:%M:%S").time()
            except ValueError:
                return self.redirect("/error?msg=Primera hora del horario incorrecta para el año.")

            try:
                if len(str_time_end) < 8:
                    str_time_end += ":00"

                time_end = datetime.strptime(str_time_end, "%H:%M:%S").time()
            except ValueError:
                return self.redirect("/error?msg=Última hora del horario incorrecta para el año.")

            try:
                time_delta = int(str_time_delta)
            except ValueError:
                return self.redirect("/error?msg=Separación entre horas incorrecta para el año.")

            # Verify dates
            if not period1_end > period1_begin:
                return self.redirect("/error?msg=Fin periodo 1 menor que comienzo para el año.")

            if not period2_end > period2_begin:
                return self.redirect("/error?msg=Fin periodo 2 menor que comienzo para el año.")

            if not period2_begin > period1_end:
                return self.redirect("/error?msg=Período 2 debe ser posterior a período 1 para el año.")

            # Verify times
            if time_delta < 10:
                return self.redirect("/error?msg=Sin sentido en separación entre horas para el año.")

            if time_begin >= time_end:
                return self.redirect("/error?msg=Hora comienzo del horario posterior a hora fin para el año.")

            # Update all existing reserves, if needed
            year = Year.retrieve()

            if move_existing_entries:
                print("*** Moving reserves")
                print("\t-- old_begin_period1:", year.period1_begin,
                      "old_end_period1:", year.period1_end)
                print("\t-  new_begin_period1:", period1_begin,
                      "new_end_period1:", period1_end)
                print("\t-- old_begin_period2:", year.period2_begin,
                      "old_end_period2:", year.period2_end)
                print("\t-  new_begin_period2:", period2_begin,
                      "new_end_period2:", period2_end)
                Reserve.move_all(old_begin_period1=year.period1_begin,
                                 old_end_period1=year.period1_end,
                                 new_begin_period1=period1_begin,
                                 new_end_period1=period1_end,
                                 old_begin_period2=year.period2_begin,
                                 old_end_period2=year.period2_end,
                                 new_begin_period2=period2_begin,
                                 new_end_period2=period2_end)

            # Update the year info
            year.name = name
            year.period_name = period_name
            year.period1_begin = period1_begin
            year.period1_end = period1_end
            year.period2_begin = period2_begin
            year.period2_end = period2_end
            year.time_begin = time_begin
            year.time_end = time_end
            year.time_delta = time_delta

            year.put()
            time.sleep(1)
            return self.redirect("/year_management")
        except Exception as e:
            logging.error("editing year", str(e))
            self.response.write("ERROR: " + str(e))


app = webapp2.WSGIApplication([
    ('/year_management', YearManagementHandler)
], debug=True)
