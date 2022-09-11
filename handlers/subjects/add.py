#!/usr/bin/env python
# esei-ra (c) baltasar 2016 MIT License <baltasarq@gmail.com>

import logging
import webapp2
from google.appengine.api import users

from model.subject import Subject


class AddSubjectHandler(webapp2.RequestHandler):
    def get(self):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        # Create the new subject
        try:
            subject = Subject(
                        name="Undefined subject name",
                        abbrev="U",
                        owner_email="nobody@atall.com")

            key = subject.put()
            return self.redirect("/subjects/modify?id=" + key.urlsafe())
        except Exception as e:
            logging.error("adding a subject", str(e))
            self.response.write("ERROR: " + str(e))


app = webapp2.WSGIApplication([
    ('/subjects/add', AddSubjectHandler)
], debug=True)
