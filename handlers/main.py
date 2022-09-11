#!/usr/bin/env python
# esei-ra (c) baltasar 2016 MIT License <baltasarq@gmail.com>


import webapp2
from webapp2_extras import jinja2
from webapp2_extras.users import users

from model.appinfo import AppInfo
from model.reserve import Reserve


class MainHandler(webapp2.RequestHandler):
    def get(self):
        usr = users.get_current_user()

        # Retrieve configurations
        str_date = self.request.GET.get("date")
        str_mode = self.request.GET.get("mode")

        template_values = {
            "users": users,
            "usr": usr,
            "info": AppInfo,
            "Reserve": Reserve,
        }

        template_values.update(Reserve.build_timetable_info(str_date, str_mode))

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("index.html", **template_values))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
