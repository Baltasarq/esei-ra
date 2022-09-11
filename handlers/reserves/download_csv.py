#!/usr/bin/env python
# esei-ra (c) baltasar 2016/20 MIT License <baltasarq@gmail.com>


import webapp2

from model.reserve import Reserve
from datetime import datetime


class DownloadReservesAsCsvHandler(webapp2.RequestHandler):
    @staticmethod
    def create_csv(values):
        toret = ""

        # First row
        first_row = "#,"

        for classroom in values["classrooms"]:
            first_row += classroom.name + ","

        toret += first_row + '\n'

        # Next rows (reserves)
        for hour_index, hour in enumerate(values["hours"]):
            row = hour.strftime("%02H:%02M") + ","

            for classroom in values["classrooms"]:
                reserves_per_classroom = values["reserves"][classroom.key]
                for reserve in reserves_per_classroom[hour_index]:
                    row += reserve.name + " "

                row += ','

            toret += row + '\n'

        return toret

    def get(self):
        # Retrieve configurations
        str_date = str(self.request.GET.get("date", ""))
        str_mode = str(self.request.GET.get("mode", ""))

        template_values = {}
        template_values.update(Reserve.build_timetable_info(str_date, str_mode))

        if not str_date:
            str_date = datetime.today().date().isoformat()

        day_of_week = Reserve.WEEK_DAYS[datetime.strptime(str_date, "%Y-%m-%d").date().isoweekday()]
        str_date = str_date.replace('-', "")

        self.response.headers["Content-Disposition"] = ("attachment;filename=esei_ra-"
                                                        + str_date + "-" + day_of_week + ".csv")
        self.response.headers["Content-Type"] = "text/csv"
        self.response.write(DownloadReservesAsCsvHandler.create_csv(template_values))


app = webapp2.WSGIApplication([
    ('/reserves/download_csv', DownloadReservesAsCsvHandler)
], debug=True)
