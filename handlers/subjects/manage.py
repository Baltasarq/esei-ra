#!/usr/bin/env python
# esei-ra (c) baltasar 2016 MIT License <baltasarq@gmail.com>

import logging
import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

from model.appinfo import AppInfo
from model.course import Course
from model.subject import Subject


class ManageSubjectsHandler(webapp2.RequestHandler):
    def get(self):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        # Render subjects
        default_course = Course.get_default()
        retrieved_subjects = Subject.query()
        orphaned_subjects = []

        # Determine orphaned subjects
        for subject in retrieved_subjects:
            if (not subject
             or not default_course
             or not subject.get_course()
             or subject.get_course().studies_name == default_course.studies_name):
                orphaned_subjects.append(subject)

        try:
            template_values = {
                "usr": usr,
                "users": users,
                "info": AppInfo,
                "Subject": Subject,
                "orphaned_subjects": orphaned_subjects,
                "courses": Course.query().order(Course.level).order(Course.studies_name)
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("subjects.html", **template_values));
        except Exception as e:
            logging.error("rendering subjects", str(e))
            self.response.write("ERROR: " + str(e))


app = webapp2.WSGIApplication([
    ('/subjects/manage', ManageSubjectsHandler)
], debug=True)
