#!/usr/bin/env python
# esei-ra (c) baltasar 2016 MIT License <baltasarq@gmail.com>


import time
import webapp2
from google.appengine.ext import ndb
from webapp2_extras.users import users

from model.reserve import Reserve


class WipeReservesHandler(webapp2.RequestHandler):
    def get(self):
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        # Delete all reserves
        reserves = Reserve.query().fetch(keys_only=True)
        ndb.delete_multi(reserves)
        time.sleep(1)

        return self.redirect("/reserves/manage")


app = webapp2.WSGIApplication([
    ('/reserves/wipe', WipeReservesHandler)
], debug=True)
