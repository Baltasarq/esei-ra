#!/usr/bin/env python
# esei-ra (c) baltasar 2016 MIT License <baltasarq@gmail.com>


import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

from model.appinfo import AppInfo
from model.course import Course
from model.subject import Subject


class ManageYearsHandler(webapp2.RequestHandler):
    def get(self):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        template_values = {
            "usr": usr,
            "users": users,
            "info": AppInfo,
            "Year": Year,
            "years": Year.query().order(-Year.period1_begin)
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("years.html", **template_values));


app = webapp2.WSGIApplication([
    ('/years/manage', ManageYearsHandler)
], debug=True)
