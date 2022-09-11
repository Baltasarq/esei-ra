#!/usr/bin/env python
# (c) esei-ra Baltasar 2016/19 MIT License <baltasarq@gmail.com>


from google.appengine.ext import ndb

from model.course import Course


class Subject(ndb.Model):
    added = ndb.DateProperty(auto_now_add=True, indexed=True)
    name = ndb.StringProperty(required=True, indexed=True)
    abbrev = ndb.StringProperty(required=True, indexed=True)
    owner_email = ndb.StringProperty(required=True, indexed=True)
    course_key = ndb.KeyProperty(kind=Course, indexed=True)

    def get_course(self):
        toret = None
        key = self.course_key

        if not key:
            toret = Course.get_default()
        else:
            toret = key.get()

        return toret

    def get_abbrev_form(self):
        str_course = (self.get_course().get_abbrev_form()
                        if self.get_course() else "??")
        return str_course + ": " + self.abbrev

    DEFAULT = None

    @staticmethod
    def get_default():
        if not Subject.DEFAULT:
            Subject.DEFAULT = Subject(name="Undefined",
                                      abbrev="UNDEF",
                                      owner_email="nobody@atall.com")

        return Subject.DEFAULT

    @staticmethod
    def retrieve(handler):
        id = handler.request.GET.get("id")
        subject = None

        if id:
            subject = ndb.Key(urlsafe=id).get()
            if not subject:
                handler.redirect("/error?msg=No subject for id: " + str(id))
        else:
            handler.redirect("/error?msg=Missing subject id.")

        return subject
