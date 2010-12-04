#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

import os
import datetime
import icalendar
from pytz.gae import pytz

ical_url = "http://www.arsenal.com/_scripts/ical.ics?tid=1006&sid=118"
london = pytz.timezone("Europe/London")

class MainHandler(webapp.RequestHandler):

    def get(self):
        result = urlfetch.fetch(ical_url)
        cal = icalendar.Calendar.from_string(result.content)
        games = []
        today = False
        for c in cal.walk('VEVENT'):
            try:
                if c["LOCATION"] == "Emirates Stadium" and c["DTSTART"].dt.date() >= datetime.date.today():
                    games.append({"StartTime":c["DTSTART"].dt.astimezone(london), "Summary": c["SUMMARY"]})
                    if c["DTSTART"].dt.date() == datetime.date.today():
                        today = True
            except KeyError:
                pass
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {"games":games, "today":today}))

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
