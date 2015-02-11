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
	'Forty Days of Rain',
	'Masacare House Party',
	'Kristen',
	'Joe Roscoe',
	'The Crowns',
	'Red Electrick', 
	'Red Electrik',
	'Maxine Pace',
	'Vandroo & Luca',
	]

def get_current_playing():
	url = 'http://www.bay.com.mt/Billboard/playing.html'
	response = urlfetch.fetch(url, headers = {'Cache-Control' : 'max-age=0'})
	
	nowPlaying = []

	if response.status_code == 200:
		raw_html = response.content
		
		# use the lxml library to convert the string to dom
		dom = html.fromstring(raw_html)

		artist = dom.get_element_by_id('playing')[0].text

		if artist is None:
			artist = ''

		nowPlaying.append(artist)

		track = dom.get_element_by_id('songname')[0].text

		if track is None:
			track = ''

		nowPlaying.append(track)
		
	return nowPlaying

def send_email(track):
	user_address = 'info@cinnamonwar.com; mawzer@gmail.com;'
	sender_address = 'mawzer@gmail.com'
	subject = track + ' Playing on 89.7 Bay!'
	body = track + ' is currently playing on 89.7 Bay! Turn it up!'

	mail.send_mail(sender_address, user_address, subject, body)

def check_last_match():
	if memcache.get("last_match") is not None:
		return True

	return False

def is_local_artist(now_playing_artist):

	for artist in local_artists:
		if artist == now_playing_artist:
			return True

	return False

def add_if_local_artist(now_playing_artist, now_playing_track):

	if not is_local_artist(now_playing_artist):
		return

	memcache.add(key="last_match", value=datetime.datetime.now(), time=300)

	songEntryDate = datetime.datetime.utcnow()

	songEntry = SongEntry(artist=now_playing_artist, track=now_playing_track, date=songEntryDate)
	songEntry.put()

class MainHandler(webapp.RequestHandler):

	def get(self):
		if check_last_match():
			self.response.out.write('Paused...')
			return

		result = get_current_playing()

		self.response.out.write('Artist: ' + result[0])
		self.response.out.write('<br />')
		self.response.out.write('Track: ' + result[1])
		self.response.out.write('<br />')

		add_if_local_artist(result[0], result[1])

		if result[0] == 'Cinnamon War':
			self.response.out.write('<br />')
			self.response.out.write('OMG!')

			send_email(result[1])

import report
from report import Report

import testmail
from testmail import TestMail

app = webapp.WSGIApplication([('/', MainHandler), ('/report', Report), ('/testmail', TestMail)], debug=True)