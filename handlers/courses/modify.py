#!/usr/bin/env python
# esei-ra (c) baltasar 2016 MIT License <baltasarq@gmail.com>


import time
import logging
import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

from model.appinfo import AppInfo
from model.course import Course


class ModifyCourseHandler(webapp2.RequestHandler):
    DEFAULT_BK_COLOR = "#808080"

    def get(self):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        # Retrieve course
        course = Course.retrieve(self)

        # Render form
        try:
            template_values = {
                "usr": usr,
                "users": users,
                "info": AppInfo,
                "course": course
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("edit_course.html", **template_values));
        except Exception as e:
            logging.error("editing course", str(e))
            self.response.write("ERROR: " + str(e))

    @staticmethod
    def handler_post(handler, course):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        if (not course):
            return self.redirect("/error?msg=Curso no encontrado.")

        # Get the data
        name = handler.request.get("edName", "").strip().upper()
        str_level = handler.request.get("edLevel", "1").strip().upper()
        bk_color = handler.request.get("edBkColor", ModifyCourseHandler.DEFAULT_BK_COLOR).strip().upper()

        # Verify
        if not name:
            return self.redirect("/error?msg=Falta nombre para el curso.")

        if not str_level:
            return self.redirect("/error?msg=Falta el #nivel.")

        if not bk_color:
            bk_color = ModifyCourseHandler.DEFAULT_BK_COLOR

        try:
            level = int(str_level)
        except ValueError:
            return self.redirect("/error?msg=Nivel incorrecto en curso.")

        # Update the course
        course.studies_name = name
        course.level = level
        course.bk_color = bk_color
        course.put()
        time.sleep(1)
        return handler.redirect("/courses/manage")

    def post(self):
        # Get the course
        course = Course.retrieve(self)

        ModifyCourseHandler.handler_post(self, course)


app = webapp2.WSGIApplication([
    ('/courses/modify', ModifyCourseHandler)
], debug=True)
