#!/usr/bin/env python
# esei-ra (c) baltasar 2016 MIT License <baltasarq@gmail.com>

import logging
import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

from model.appinfo import AppInfo
from model.classroom import Classroom


class ManageClassroomsHandler(webapp2.RequestHandler):
    def get(self):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        # Render classrooms
        classrooms = Classroom.query()\
                        .order(Classroom.floor)\
                        .order(Classroom.building)\
                        .order(Classroom.name)

        try:
            template_values = {
                "usr": usr,
                "users": users,
                "info": AppInfo,
                "classrooms": classrooms,
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("classrooms.html", **template_values));
        except Exception as e:
            logging.error("rendering classrooms", str(e))
            self.response.write("ERROR: " + str(e))


app = webapp2.WSGIApplication([
    ('/classrooms/manage', ManageClassroomsHandler)
], debug=True)
