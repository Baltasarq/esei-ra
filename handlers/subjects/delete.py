#!/usr/bin/env python
# esei-ra (c) baltasar 2016 MIT License <baltasarq@gmail.com>

import time
import webapp2
from webapp2_extras.users import users

from model.subject import Subject


class DeleteSubjectHandler(webapp2.RequestHandler):
    def get(self):
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        # Delete course
        course = Subject.retrieve(self)
        course.key.delete()
        time.sleep(1)

        return self.redirect("/subjects/manage")


app = webapp2.WSGIApplication([
    ('/subjects/delete', DeleteSubjectHandler)
], debug=True)
