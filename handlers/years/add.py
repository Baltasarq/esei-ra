#!/usr/bin/env python
# esei-ra (c) baltasar 2016 MIT License <baltasarq@gmail.com>


import webapp2
from google.appengine.api import users
from datetime import datetime

from model.year import Year


class AddYearHandler(webapp2.RequestHandler):
    def get(self):
        # Get the usr
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        # Create the new subject
        year = Year.create(datetime(1992, 9, 1))
        key = year.put()
        return self.redirect("/years/modify?id=" + key.urlsafe())


app = webapp2.WSGIApplication([
    ('/years/add', AddYearHandler)
], debug=True)
