''' Scraper that scrapes bruinwalk.com for class ratings. '''

import csv
import os
from multiprocessing.dummy import Pool as ThreadPool
import re
import string
import sys
import requests
from lxml import html

''' Stores the data for each class '''
class ClassRatingData:
	def __init__(self, class_name, class_rating):
		self.class_name = class_name
		self.class_rating = class_rating

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

def switch_statement(number):
	return {
		0: '1',
		1: '3',
		2: '5',
		3: '8',
		4: '10',
		5: '12',
		6: '15',
		7: '17',
		8: '19',
		9: '22',
	}[number]

def get_class_rating(page, number):
	tree = html.fromstring(page.content)
	xPath = "/html/body/section/div/section/div[2]/div[2]/div[4]/div[" + switch_statement(number) + "]/div/div[1]/span/b//text()"
	classRating = tree.xpath(xPath)
	return classRating

def get_class_list(url):
	page = get_page(url)
	html = page.text
	html = html.replace('amp;', '')
#	print html
	classNameRegEx1 = '<div class="title circle main">(.+?)</div>'
	classNamePattern1 = re.compile(classNameRegEx1)
	classNamesAllClasses = re.findall(classNamePattern1, html)
	class_rating_list = list()
	i=0
	j=0
	while j<len(classNamesAllClasses):
		class_rating_list.append(ClassRatingData(classNamesAllClasses[j], get_class_rating(page, i)))
		j += 2
		i += 1
		if(i==10):
			i=0
	return class_rating_list

''' writes the class ratings to csv files '''
def write_to_csv(class_rating_list):
	os_dir = os.path.dirname(__file__)
	class_rating_filename = os.path.join( \
        os_dir, '../ClassSchedulizer/db/class_rating_data.csv')
	class_rating_file = open(class_rating_filename, 'w')
	class_rating_writer = csv.writer(class_rating_file, delimiter=',', \
        lineterminator='\r\n', quoting=csv.QUOTE_ALL)
	class_rating_writer.writerow(( \
        "class_name", "class_rating"))
	for each_class in class_rating_list:
		print "Writing data for " + each_class.class_name + " to file."
		className = each_class.class_name
		classRating = each_class.class_rating
		class_rating_writer.writerow((each_class.class_name, each_class.class_rating))
	class_rating_file.close()


i=1
while(i<=100):
	url = "http://www.bruinwalk.com/search/?sort=alphabetical&category=classes&page=" + str(i)
	classRatings = get_class_list(url)
	write_to_csv(classRatings)
	i += 1

#classRatings = get_class_list("http://www.bruinwalk.com/search/?sort=alphabetical&category=classes&page=1")
#write_to_csv(classRatings)


#	i =1
######################################change back to 100
#	while(i<=100):
#		url = "http://www.bruinwalk.com/search/?sort=alphabetical&category=classes&page=" + str(i)
#		get_class_name_and_rating(url)
#		i += 1








# to test get_page()
#get_page('http://www.bruinwalk.com')


''' Extracts the class name from a url. '''
def get_class_name_and_rating(url):
	page = get_page(url)
	html = page.text
#	print html

	classNameRegEx1 = '<div class="title circle main">(.+?)</div>'
	classNamePattern1 = re.compile(classNameRegEx1)
	classNamesAllClasses = re.findall(classNamePattern1, html)

	i=0
	j=0
	while j<len(classNamesAllClasses):
		print classNamesAllClasses[j]
		classRating = get_class_rating(page, i)
		print classRating
		j += 2
		i += 1
		if(i==10):
			i=0




#get_class_name_and_rating("http://www.bruinwalk.com/search/?sort=alphabetical&category=classes&page=1")
#get_class_name_and_rating("http://www.bruinwalk.com/search/?sort=alphabetical&category=classes&page=2")
#get_class_name_and_rating("http://www.bruinwalk.com/search/?sort=alphabetical&category=classes&page=3")




def output_all_class_names():
	i =1
######################################change back to 100
	while(i<=100):
		url = "http://www.bruinwalk.com/search/?sort=alphabetical&category=classes&page=" + str(i)
		get_class_name_and_rating(url)
		i += 1








#reload(sys)
#sys.setdefaultencoding('utf-8')
#output_all_class_names()

# ratings = get_all_class_names_and_ratings()
# write_to_csv(ratings)
