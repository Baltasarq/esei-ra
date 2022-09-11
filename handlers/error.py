#!/usr/bin/env python
# CnEscualos (c) baltasar 2016/19 MIT License <baltasarq@gmail.com>


import logging
import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

from model.appinfo import AppInfo


class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        # Retrieve message
        try:
            msg = self.request.GET['msg']
        except:
            msg = None

        if not msg:
            msg = "CRITICAL - contact development team"

        # Render
        try:
            template_values = {
                "kind": "Error",
                "users": users,
                "usr": users.get_current_user(),
                "msg": msg,
                "info": AppInfo
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("error.html", **template_values));
        except Exception as e:
            logging.error(str(e))
            self.response.write("ERROR: " + str(e))


app = webapp2.WSGIApplication([
    ("/error", ErrorHandler),
], debug=True)
