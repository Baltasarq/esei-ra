#!/usr/bin/env python
# esei-ra (c) baltasar 2016 MIT License <baltasarq@gmail.com>

import logging
import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

from model.appinfo import AppInfo
from model.classroom import Classroom
from model.subject import Subject
from model.reserve import Reserve


class ManageReservesHandler(webapp2.RequestHandler):
    def get(self):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        # Render reserves
        default_classroom = Classroom.get_default()
        default_subject = Subject.get_default()
        retrieved_reserves = Reserve.query()
        orphaned_reserves = []

        # Determine orphaned subjects
        for reserve in retrieved_reserves:
            reserve_subject = reserve.get_subject()
            reserve_classroom = reserve.get_classroom()

            if (reserve_subject.abbrev == default_subject.abbrev
             or reserve_classroom.name == default_classroom.name):
                orphaned_reserves.append(reserve)

        try:
            template_values = {
                "usr": usr,
                "users": users,
                "info": AppInfo,
                "Reserve": Reserve,
                "classrooms": Classroom.query().order(Classroom.floor).order(Classroom.building).order(Classroom.name),
                "orphaned_reserves": orphaned_reserves
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("reserves.html", **template_values));
        except Exception as e:
            logging.error("rendering reserves", str(e))
            self.response.write("ERROR: " + str(e))


app = webapp2.WSGIApplication([
    ('/reserves/manage', ManageReservesHandler)
], debug=True)
