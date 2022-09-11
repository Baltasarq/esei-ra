#!/usr/bin/env python
# esei-ra (c) baltasar 2016 MIT License <baltasarq@gmail.com>

import logging
import webapp2
from google.appengine.api import users

from model.classroom import Classroom


class AddClassroomHandler(webapp2.RequestHandler):
    def get(self):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        # Create the new classroom
        try:
            classroom = Classroom(
                        name="Undefined",
                        building="Unknown",
                        floor=0,
                        pax=0)

            key = classroom.put()
            return self.redirect("/classrooms/modify?id=" + key.urlsafe())
        except Exception as e:
            logging.error("adding a classroom", str(e))
            self.response.write("ERROR: " + str(e))


app = webapp2.WSGIApplication([
    ('/classrooms/add', AddClassroomHandler)
], debug=True)
