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

import datetime
import songentry

from songentry import SongEntry

from operator import itemgetter, attrgetter

local_artists = [
	'Cinnamon War', 
	'Airport Impressions', 
	'Gianluca Bezzina', 
	'Malcolm Pisani', 
	'The Shh', 
	'Winter Moods', 
	'Ira Losco', 
	'Chess', 
	'Daniel Testa', 
	'Giorgio Armani', 
	'Plan Zero', 
	'Chris And Moira', 
	'Tenishia', 
	'Dana Mc Keon', 
	'Sophie', 
	'The Kite Project', 
	'Domino Effect',
	'Vandroo & Luca ft. Yazmin Helledie',
	'Norbert',
	'Waterwings',
	'Forty Days Of Rain',
	'Masacre House Party',
	'Kristen',
	'Joe Roscoe',
	'The Crowns',
	'Red Electrick', 
	'Red Electrik' 
	]
	
class ChartEntry:
	songEntry = None
	count = 0

class Report(webapp.RequestHandler):
	def generate_chart(self):
		chartEntries = []

		for artist in local_artists:
			songEntries = db.GqlQuery("SELECT * FROM SongEntry WHERE artist = '" + artist + "'")
	
			if songEntries.count() == 0:
				continue

			songEntry = songEntries[0]

			chartEntry = ChartEntry()
			chartEntry.songEntry = songEntry
			chartEntry.count = songEntries.count()

			chartEntries.append(chartEntry)

		chartEntries = sorted(chartEntries, key=attrgetter('count'), reverse=True)
		
		pos = 1

		for chartEntry in chartEntries:
			self.response.out.write(str(pos) + '. ' + chartEntry.songEntry.artist + ' - ' + chartEntry.songEntry.track)
			self.response.out.write(' ' + str(chartEntry.count))
			self.response.out.write('<br />')

			pos += 1

	def get(self):		
		self.generate_chart()

		songEntries = db.GqlQuery("SELECT * FROM SongEntry ORDER BY date DESC")

		self.response.out.write('<br /><br />')

		for songEntry in songEntries:
			adjusted_datetime = songEntry.date + datetime.timedelta(hours = 2)

			self.response.out.write('Artist: ' + songEntry.artist)
			self.response.out.write('<br />')
			self.response.out.write('Track: ' + songEntry.track)
			self.response.out.write('<br />')
			self.response.out.write('Date: ' + adjusted_datetime.strftime('%c'))
			self.response.out.write('<br /><br />')

