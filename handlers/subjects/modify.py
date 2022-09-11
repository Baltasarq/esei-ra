#!/usr/bin/env python
# encoding: utf-8
# esei-ra (c) baltasar 2016 MIT License <baltasarq@gmail.com>


import time
import logging
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
from webapp2_extras import jinja2

from ..utils import semi_title
from model.appinfo import AppInfo
from model.course import Course
from model.subject import Subject


class ModifySubjectHandler(webapp2.RequestHandler):
    def get(self):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        # Retrieve subject
        subject = Subject.retrieve(self)

        # Retrieve courses
        all_courses = Course.query().order(Course.studies_name).order(Course.level)

        # Render subjects
        try:
            template_values = {
                "usr": usr,
                "users": users,
                "info": AppInfo,
                "subject": subject,
                "course_of_subject": subject.get_course(),
                "all_courses": all_courses
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("edit_subject.html", **template_values));
        except Exception as e:
            logging.error("editing subjects", str(e))
            self.response.write("ERROR: " + str(e))

    def post(self):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        try:
            # Get the subject
            subject = Subject.retrieve(self)

            # Get the data
            name = semi_title(self.request.get("edName", "").strip())
            owner_email = self.request.get("edOwnerEmail", "").strip()
            abbrev = self.request.get("edAbbrev", "").strip().upper()
            course_id = self.request.get("edCourse", "").strip()

            # Verify
            if not name:
                return self.redirect("/error?msg=Falta nombre para el curso.")

            if not owner_email:
                return self.redirect("/error?msg=Falta e.mail del responsable para el curso.")

            if not abbrev:
                return self.redirect("/error?msg=Falta abreviatura para el curso.")

            if not course_id:
                course_key = None
            else:
                course_key = ndb.Key(urlsafe=course_id)

            # Update the subject
            subject.name = name
            subject.owner_email = owner_email
            subject.abbrev = abbrev
            subject.course_key = course_key
            subject.put()
            time.sleep(1)
            return self.redirect("/subjects/manage")
        except Exception as e:
            logging.error("editing subjects", str(e))
            self.response.write("ERROR: " + str(e))


app = webapp2.WSGIApplication([
    ('/subjects/modify', ModifySubjectHandler)
], debug=True)
