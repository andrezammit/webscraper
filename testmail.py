#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from google.appengine.ext import db, webapp
from google.appengine.api import memcache, mail, urlfetch

from lxml import html

class TestMail(webapp.RequestHandler):
	def send_email(self, track):
		user_address = 'info@cinnamonwar.com; mawzer@gmail.com;'
		sender_address = 'mawzer@gmail.com'
		subject = track + ' Playing on 89.7 Bay!'
		body = track + ' is currently playing on 89.7 Bay! Turn it up!'

		mail.send_mail(sender_address, user_address, subject, body)

	def get(self):
		self.send_email('Test')
