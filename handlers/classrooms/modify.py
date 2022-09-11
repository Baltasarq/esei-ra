#!/usr/bin/env python
# esei-ra (c) baltasar 2016 MIT License <baltasarq@gmail.com>

import time
import logging
import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

from model.appinfo import AppInfo
from model.classroom import Classroom


class ModifyClassroomHandler(webapp2.RequestHandler):
    def get(self):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        # Retrieve classroom
        classroom = Classroom.retrieve(self)

        # Render subjects
        try:
            template_values = {
                "usr": usr,
                "users": users,
                "info": AppInfo,
                "classroom": classroom
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("edit_classroom.html", **template_values));
        except Exception as e:
            logging.error("editing classroom", str(e))
            self.response.write("ERROR: " + str(e))

    def post(self):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        try:
            # Get the classroom
            subject = Classroom.retrieve(self)

            # Get the data
            name = self.request.get("edName", "").strip().upper()
            abbrev = self.request.get("edAbbrev", "").strip().upper()
            building = self.request.get("edBuilding", "").strip().title()
            str_floor = self.request.get("edFloor", "1").strip()
            str_pax = self.request.get("edPax", "1").strip()
            str_mode = self.request.get("edPract", "False").strip()

            # Verify
            if not name:
                return self.redirect("/error?msg=Falta nombre para el aula.")

            if not abbrev:
                return self.redirect("/error?msg=Falta abreviatura para el aula.")

            if not building:
                return self.redirect("/error?msg=Falta el edificio para el aula.")

            try:
                floor = int(str_floor)
            except ValueError:
                return self.redirect("/error?msg=Piso incorrecto en aula.")

            try:
                pax = int(str_pax)
            except ValueError:
                return self.redirect("/error?msg=Plazas incorrectas en aula.")

            try:
                mode = (str_mode == "True")
            except ValueError:
                mode = False

            # Update the classroom
            subject.name = name
            subject.abbrev = abbrev
            subject.building = building
            subject.floor = floor
            subject.pax = pax
            subject.pract = mode
            subject.put()
            time.sleep(1)
            return self.redirect("/classrooms/manage")
        except Exception as e:
            logging.error("editing classroom", str(e))
            self.response.write("ERROR: " + str(e))


app = webapp2.WSGIApplication([
    ('/classrooms/modify', ModifyClassroomHandler)
], debug=True)
