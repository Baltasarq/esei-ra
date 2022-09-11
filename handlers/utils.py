#!/usr/bin/env python
# encoding: utf-8
# esei-ra (c) baltasar 2019 MIT License <baltasarq@gmail.com>


def semi_title(s):
    """Returns a new string in which every word is capitalized,
       except prepositions and articles."""

    PREPS_DETS = u" eso esto aquel \
              uno una unos unas \
              esa esta aquella \
              esos estos ellos \
              esas estas aquellas \
              ese este ello aquello \
              del para por con pro \
              ante bajo cabe contra mas \
              desde hacia hasta \
              durante mediante para \
              sin sobre tras versus vía según \
              los las "
    ABBREV = u" tic bbdd so bd i ii iii iv v vi vii viii ix x "
    toret = ""

    if s:
        parts = unicode(s).strip().split()
        isFirst = True

        for part in parts:
            part = part.lower()

            if part:
                part = " " + part + " "

                if part in ABBREV:
                    toret += " " + part.strip().upper()
                else:
                    if (isFirst
                    or (len(part) > 4 and part not in PREPS_DETS)):
                        toret += " " + part.strip().title()
                    else:
                        toret += " " + part.strip()

                isFirst = False

    return toret.strip()


if __name__ == "__main__":
    print(semi_title(u"unas gestiones y Configuración del Software para las TIC de estos lares ii"))
