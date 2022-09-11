#!/usr/bin/env python
# esei-ra (c) baltasar 2016 MIT License <baltasarq@gmail.com>

import time
import webapp2
from webapp2_extras.users import users

from model.reserve import Reserve


class DeleteReserveHandler(webapp2.RequestHandler):
    def get(self):
        usr = users.get_current_user()

        if (not usr
         or not users.is_current_user_admin()):
            return self.redirect("/error?msg=No eres admin.")

        # Delete course
        reserve = Reserve.retrieve(self)
        date_begin = reserve.date_begin
        week_day = reserve.week_day
        reserve.key.delete()
        time.sleep(1)

        date_begin = Reserve.get_date_of_next_week_day_from(date_begin, week_day)
        return self.redirect("/?date="
                             + Reserve.str_from_date(date_begin))


app = webapp2.WSGIApplication([
    ('/reserves/delete', DeleteReserveHandler)
], debug=True)
