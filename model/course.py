#!/usr/bin/env python
# encoding: utf-8
# (c) esei-ra Baltasar 2016/19 MIT License <baltasarq@gmail.com>


from google.appengine.ext import ndb


class Course(ndb.Model):
    added = ndb.DateProperty(auto_now_add=True, indexed=True)
    level = ndb.IntegerProperty(indexed=True, required=True)
    studies_name = ndb.StringProperty(indexed=True, required=True)
    bk_color = ndb.StringProperty(default="#808080")

    def get_abbrev_form(self):
        return self.studies_name + str(self.level)

    def __str__(self):
        return str(self.level) + "/ " + self.studies_name

    DEFAULT = None

    @staticmethod
    def get_default():
        if not Course.DEFAULT:
            Course.DEFAULT = Course(level=1, studies_name="ZZ_default")

        return Course.DEFAULT

    @staticmethod
    def retrieve(handler):
        id = handler.request.GET.get("id")
        course = None

        if id:
            course = ndb.Key(urlsafe=id).get()
            if not course:
                handler.redirect("/error?msg=No course for id: " + str(id))
        else:
            handler.redirect("/error?msg=Missing course id.")

        return course
