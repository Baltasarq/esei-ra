#!/usr/bin/env python
# esei-ra (c) baltasar 2016/20 MIT License <baltasarq@gmail.com>


import webapp2
from webapp2_extras import jinja2

from model.reserve import Reserve
from datetime import datetime


class DownloadReservesAsXlsHandler(webapp2.RequestHandler):
    def get(self):
        # Retrieve configurations
        str_date = str(self.request.GET.get("date", ""))
        str_mode = str(self.request.GET.get("mode", ""))

        template_values = {}
        template_values.update(Reserve.build_timetable_info(str_date, str_mode))

        if not str_date:
            str_date = datetime.today().date().isoformat()

        date = datetime.strptime(str_date, "%Y-%m-%d").date()
        day_of_week = Reserve.WEEK_DAYS[date.isoweekday()]
        str_date = str_date.replace('-', "")
        template_values["day_of_week"] = day_of_week
        template_values["date"] = date
        template_values["current_time"] = datetime.today().time()

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.headers["Content-Disposition"] = ("attachment;filename=esei_ra-"
                                                        + str_date + "-" + day_of_week + ".xls")
        self.response.headers["Content-Type"] = "application/vnd.ms-excel"
        self.response.write(jinja.render_template("template_excel.xls.txt", **template_values))


app = webapp2.WSGIApplication([
    ('/reserves/download_xls', DownloadReservesAsXlsHandler)
], debug=True)
