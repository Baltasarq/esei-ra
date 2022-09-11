#!/usr/bin/env python
# (c) esei-ra Baltasar 2016/19 MIT License <baltasarq@gmail.com>


from google.appengine.ext import ndb


class Classroom(ndb.Model):
    added = ndb.DateProperty(auto_now_add=True, indexed=True)
    name = ndb.StringProperty(required=True, indexed=True)
    abbrev = ndb.StringProperty(default="CLS")
    building = ndb.StringProperty(required=True, indexed=True)
    pract = ndb.BooleanProperty(default=False, indexed=True)
    floor = ndb.IntegerProperty(required=True, indexed=True)
    pax = ndb.IntegerProperty(default=20, indexed=True)

    def get_pract_as_str(self):
        return "P" if self.pract else "T"

    DEFAULT = None

    @staticmethod
    def get_default():
        if not Classroom.DEFAULT:
            Classroom.DEFAULT = Classroom(name="Undefined",
                                      building="Unknown",
                                      floor=0,
                                      pax=0)

        return Classroom.DEFAULT

    @staticmethod
    def retrieve(handler):
        id = handler.request.GET.get("id")
        classroom = None

        if id:
            classroom = ndb.Key(urlsafe=id).get()
            if not classroom:
                handler.redirect("/error?msg=No classroom for id: " + str(id))
        else:
            handler.redirect("/error?msg=Missing classroom id.")

        return classroom
