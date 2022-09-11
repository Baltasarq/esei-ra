#!/usr/bin/env python
# coding: utf-8
# esei-ra (c) baltasar 2016 MIT License <baltasarq@gmail.com>

import time
from datetime import datetime
from datetime import timedelta
import logging
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users
from webapp2_extras import jinja2

from model.appinfo import AppInfo
from model.reserve import Reserve
from model.classroom import Classroom
from model.subject import Subject
from model.year import Year


class ModifyReserveHandler(webapp2.RequestHandler):
    def get(self):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        # Retrieve reserve
        reserve = Reserve.retrieve(self)

        # Render year
        try:
            template_values = {
                "usr": usr,
                "users": users,
                "info": AppInfo,
                "classrooms": Classroom.query().order(Subject.name),
                "subjects": Subject.query().order(Subject.name),
                "Reserve": Reserve,
                "reserve": reserve,
                "subject_of_reserve": reserve.get_subject(),
                "classroom_of_reserve": reserve.get_classroom(),
                "year": Year.retrieve()
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("edit_reserve.html", **template_values));
        except Exception as e:
            logging.error("editing reserve", str(e))
            self.response.write("ERROR: " + str(e))

    def post(self):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        try:
            # Get the data
            name = self.request.get("edName", "").strip()
            str_week_day = self.request.get("edWeekDay", "0").strip()
            classroom_id = self.request.get("edClassroom", "").strip()
            subject_id = self.request.get("edSubject", "").strip()
            str_date_begin = self.request.get("edDateBegin", "2000-09-01").strip()
            str_date_end = self.request.get("edDateEnd", "2001-01-31").strip()
            str_time_begin = self.request.get("edTimeBegin", "09:00:00").strip()
            str_time_end = self.request.get("edTimeEnd", "10:00:00").strip()
            str_chk_clashes = self.request.get("chkChekClashes", "")
            str_chk_copy = self.request.get("chkCopy", "")
            notes = self.request.get("edNotes", "").strip()

            # Get the reserve
            if str_chk_copy:
                reserve = Reserve()
            else:
                reserve = Reserve.retrieve(self)

            # Verify
            if not name:
                return self.redirect("/error?msg=Falta nombre para la reserva.")

            if not str_week_day:
                return self.redirect("/error?msg=Falta el día de la semana para la reserva.")

            try:
                if len(str_time_begin) < 8:
                    str_time_begin += ":00"

                date_begin = datetime.strptime(str_date_begin, "%Y-%m-%d").date()
                time_begin = datetime.strptime(str_time_begin, "%H:%M:%S").time()
            except ValueError:
                return self.redirect("/error?msg=Comienzo reserva incorrecto.")

            try:
                if len(str_time_end) < 8:
                    str_time_end += ":00"

                date_end = datetime.strptime(str_date_end, "%Y-%m-%d").date()
                time_end = datetime.strptime(str_time_end, "%H:%M:%S").time()
            except ValueError:
                return self.redirect("/error?msg=Final reserva incorrecto.")

            try:
                week_day = int(str_week_day)
            except ValueError:
                week_day = 0

            classroom_key = None
            if classroom_id:
                classroom_key = ndb.Key(urlsafe=classroom_id)

            subject_key = None
            if subject_id:
                subject_key = ndb.Key(urlsafe=subject_id)

            if not date_end > date_begin:
                return self.redirect("/error?msg=Fecha final debe ser posterior al comienzo en reserva.")

            if not time_end > time_begin:
                return self.redirect("/error?msg=Hora final debe ser posterior al comienzo para la reserva.")

            # Chk availability
            conflicting_reserves = []
            if str_chk_clashes == "on":
                queried_reserves = Reserve.query(Reserve.classroom_key == classroom_key).fetch()

                for conflict_reserve in queried_reserves:
                    if conflict_reserve.key == reserve.key:
                        continue

                    if (conflict_reserve.date_begin <= date_begin <= conflict_reserve.date_end
                     or conflict_reserve.date_begin <= date_end <= conflict_reserve.date_end):
                        if week_day != 0 and conflict_reserve.week_day != 0:
                            if (conflict_reserve.is_a_match_for_week_day(week_day)
                            and conflict_reserve.is_a_match_for_time(time_begin)):
                                conflicting_reserves.append(conflict_reserve)
                        else:
                            delta = timedelta(days=1)
                            the_date = date_begin if date_begin > conflict_reserve.date_begin else conflict_reserve.date_begin
                            end_date = date_end if date_end < conflict_reserve.date_end else conflict_reserve.date_end

                            while the_date < end_date:
                                if conflict_reserve.is_a_match_for_time(time_begin):
                                    conflicting_reserves.append(conflict_reserve)
                                    break

                                the_date += delta

            if not conflicting_reserves:
                # Update the reserve
                reserve.name = name
                reserve.classroom_key = classroom_key
                reserve.subject_key = subject_key
                reserve.week_day = week_day
                reserve.date_begin = date_begin
                reserve.date_end = date_end
                reserve.time_begin = time_begin
                reserve.time_end = time_end
                reserve.notes = notes

                reserve.put()
                time.sleep(1)
                date_begin = Reserve.get_date_of_next_week_day_from(date_begin, week_day)
                return self.redirect("/?date="
                                     + Reserve.str_from_date(date_begin))
            else:
                template_values = {
                    "usr": usr,
                    "users": users,
                    "info": AppInfo,
                    "reserves": conflicting_reserves,
                }

                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("conflicting_reserves.html", **template_values));
        except Exception as e:
            logging.error("modifying reserve", str(e))
            self.response.write("ERROR: " + str(e))


app = webapp2.WSGIApplication([
    ('/reserves/modify', ModifyReserveHandler)
], debug=True)
