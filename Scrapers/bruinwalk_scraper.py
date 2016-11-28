''' Scraper that scrapes bruinwalk.com for class ratings. '''

import csv
import os
from multiprocessing.dummy import Pool as ThreadPool
import re
import string
import sys
import requests
from lxml import html

''' Stores the data for each professor: professor name, overall professor rating, easiness rating, workload rating, clarity rating, and helpfulness rating  '''
class Professor:
	def __init__(self, professor_name):
		self.professor_name = professor_name
		self.overall = ""
		self.easiness = ""
		self.workload = ""
		self.clarity = ""
		self.helpfulness = ""

''' Stores the data for each class: class name, overall class rating, and a list of professors  '''
class ClassRatingData:
	def __init__(self, class_name, class_rating):
		self.class_name = class_name
		self.class_rating = class_rating
		self.professors = list()

''' Returns the page for a given url. Retries up to 10 times to retrieve the page. '''
def get_page(url):
	page = None
	max_tries = 10
	while page is None:
		try:
			page = requests.get(url)
		except Exception:
			print "Connection aborted... trying again"
			max_tries -= 1
			if max_tries == 0:
				raise Exception('Connection aborted 10 times for ' + url)
	return page

''' Dictionary used as a switch statement to convert the class number on the given webpage to the element number of its title in the blue cirlce. Helps grab the correct class rating. '''
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

''' Gets the class rating for the given class by using its xpath '''
def get_class_rating(page, number):
	tree = html.fromstring(page.content)
	xPath = "/html/body/section/div/section/div[2]/div[2]/div[4]/div[" + switch_statement(number) + "]/div/div[1]/span/b//text()"
	classRating = tree.xpath(xPath)
	return classRating

''' Returns a list of Professor objects, which contains the professor name, overall professor rating, easiness rating, workload rating, clarity rating, and helpfulness rating   '''
def get_professors(class_name):
	list_of_professors = list()
	class_name = class_name.replace(' ', '-')
	classURLName = class_name.lower()
	url = "http://www.bruinwalk.com/classes/" + classURLName
	page = get_page(url)
	html1 = page.text
	html1 = html1.replace('amp;', '')
	professorNameRegEx = '<span class="prof name">(.+?)</span>' 
	professorNamePattern = re.compile(professorNameRegEx)
	allProfessorNames = re.findall(professorNamePattern, html1)
	tree = html.fromstring(page.content)
	xPath = "//div[@class='hide-for-small-only']//td[@class='rating-cell']//span//text()"
	allProfessorsRatings = tree.xpath(xPath)
	i = 0
	j=0
	while (i < len(allProfessorNames)):
		professorInstance = Professor(allProfessorNames[i])
		professorInstance.overall = allProfessorsRatings[j]
		professorInstance.easiness = allProfessorsRatings[j+1]
		professorInstance.workload = allProfessorsRatings[j+2]
		professorInstance.clarity = allProfessorsRatings[j+3]
		professorInstance.helpfulness = allProfessorsRatings[j+4]
		j = j+5
		i += 2
		list_of_professors.append(professorInstance)
	return list_of_professors


''' Returns a list of ClassRatingData objects, which contains the class name and class rating.  '''
def get_class_list(url):
	class_rating_list = list()	
	page = get_page(url)
	html = page.text
	html = html.replace('amp;', '')
	classNameRegEx1 = '<div class="title circle main">(.+?)</div>'
	classNamePattern1 = re.compile(classNameRegEx1)
	classNamesAllClasses = re.findall(classNamePattern1, html)
	i=0
	j=0
	while j<len(classNamesAllClasses):
		classRatingDataInstance = ClassRatingData(classNamesAllClasses[j], get_class_rating(page, i))
		classRatingDataInstance.professors = get_professors(classRatingDataInstance.class_name)
		class_rating_list.append(classRatingDataInstance)
		j += 2
		i += 1
		if(i==10):
			i=0
	return class_rating_list

''' Writes the class ratings to csv files '''
def write_to_csv(class_rating_list, counter):
	os_dir = os.path.dirname(__file__)
	class_rating_filename = os.path.join( \
        os_dir, '../ClassSchedulizer/lib/seeds/class_rating_data.csv')
	class_rating_file = open(class_rating_filename, 'a')
	class_rating_writer = csv.writer(class_rating_file, delimiter=',', \
        lineterminator='\r\n', quoting=csv.QUOTE_ALL)	
	if (counter == 0):
		class_rating_writer.writerow(( \
        "class_name", "class_rating", "professor_name", "overall", "easiness", "workload", "clarity", "helpfulness"))
        counter += 1
 	n=0
	for each_class in class_rating_list:
		for each_professor in each_class.professors:
			print "Writing data for " + each_class.class_name + " to file."
			className = each_class.class_name
			classRating = each_class.class_rating[0]
			professorName = each_professor.professor_name
			overall = each_professor.overall
			easiness = each_professor.easiness
			workload = each_professor.workload
			clarity = each_professor.clarity
			helpfulness = each_professor.helpfulness
			class_rating_writer.writerow((className, classRating, professorName, overall, easiness, workload, clarity, helpfulness))
			n += 1
	class_rating_file.close()

''' Main function '''
if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	i=9
	j=1
	counter = 0
	while (i <300):
		while (j < 55):
			url = "http://www.bruinwalk.com/search/?category=classes&dept=" + str(i) + "&page=" + str(j)
			classRatings = get_class_list(url)
			if len(classRatings) == 0:
				break;
			write_to_csv(classRatings, counter)
			counter += 1
			j += 1
		i += 1
		j=1
