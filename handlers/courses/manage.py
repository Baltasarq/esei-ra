#!/usr/bin/env python
# esei-ra (c) baltasar 2016 MIT License <baltasarq@gmail.com>

import time
import logging
import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

from model.appinfo import AppInfo
from model.course import Course
from handlers.courses.modify import ModifyCourseHandler


class ShowCoursesHandler(webapp2.RequestHandler):
    def get(self):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        # Render courses
        try:
            template_values = {
                "usr": usr,
                "users": users,
                "info": AppInfo,
                "courses": Course.query().order(Course.studies_name).order(Course.level)
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("courses.html", **template_values));
        except Exception as e:
            logging.error("rendering courses", str(e))
            self.response.write("ERROR: " + str(e))

    def post(self):
        return ModifyCourseHandler.handler_post(self, Course())


app = webapp2.WSGIApplication([
    ('/courses/manage', ShowCoursesHandler)
], debug=True)
