''' Scraper that scrapes bruinwalk.com for class ratings. '''

import csv
import os
from multiprocessing.dummy import Pool as ThreadPool
import re
import string
import sys
import requests


''' Stores the data for each class '''
class ClassRatingData:
	def _init_(self, class_name, website_title, url):
		self.class_name = class_name
		self.website_title = website_title
		self.url = url

''' Returns the page for a given url. Retries up to 10 times to retrieve the page. '''
def get_page(url):
	page = None
	max_tries = 10
	while page is None:
		try:
			page = requests.get(url)
#			to print html of page
#			print page.text 
		except Exception:
			print "Connection aborted... trying again"
			max_tries -= 1
			if max_tries == 0:
				raise Exception('Connection aborted 10 times for ' + url)
	return page

# to test get_page()
#get_page('http://www.bruinwalk.com')


''' Extracts the class name from a url. '''
def get_class_name_and_rating(url):
	page = get_page(url)
	html = page.text
#	print html

	classNameRegEx1 = '<div class="title circle main">(.+?)</div>'
	classNameRegEx2 = '<div class="title circle">(.+?)</div>'
	classNamePattern1 = re.compile(classNameRegEx1)
	classNamePattern2 = re.compile(classNameRegEx2)

	classNamesAllClasses = re.findall(classNamePattern1, html)
	classNameFromClassPage = re.findall(classNamePattern2, html)
	
	classRatingRegEx1 = '<span class="rating"><b>(.+?)</b><i>Overall rating</i></span>'
	classRatingPattern1 = re.compile(classRatingRegEx1)

	classRatingAllClasses = re.findall(classRatingPattern1, html)
	print classRatingAllClasses

	j=0
	i=0
	while j<len(classNamesAllClasses):
		print classNamesAllClasses[j]
#		print classRatingAllClasses[i]
		j += 2
#		i += 1

get_class_name_and_rating("http://www.bruinwalk.com/search/?sort=alphabetical&category=classes&page=1")
#get_class_name_and_rating("http://www.bruinwalk.com/search/?sort=alphabetical&category=classes&page=2")
#get_class_name_and_rating("http://www.bruinwalk.com/search/?sort=alphabetical&category=classes&page=3")







