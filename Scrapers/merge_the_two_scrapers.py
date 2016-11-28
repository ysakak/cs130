''' Merge two scrapers' data together '''

''' check class name similiarity 75%>, then check professor similiarity 75%>,

 create a map, grab all independent class data, check that with every class i have on bruinwalk scraper 100percent title match
 instr 75% >
 append the id to bruinwalk scraper csv row'''


import csv
import os
from multiprocessing.dummy import Pool as ThreadPool
import re
import string
import sys
import requests
from lxml import html
from fuzzywuzzy import fuzz
from fuzzywuzzy import process




''' defines a pair of instructor and lecture_id'''
class InstructorLectureIDPair:
	def __init__(self, instructor, lecture_id):
		self.instructor = instructor
		self.lecture_id = lecture_id




'''open/read registrars inded classes csv file'''
os_dir = os.path.dirname(__file__)
independent_classes_filename = os.path.join( \
        os_dir, '../ClassSchedulizer/lib/seeds/independent_class_data.csv')
independent_classes_file = open(independent_classes_filename, 'r')
independent_classes_reader = csv.reader(independent_classes_file, delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_ALL)
next(reader, None) # skip headers




#dictionary of every class title to a pair (of instructor and lecture id)
dictionary = dict()
for each_row in independent_classes_reader:
	course_id = each_row[3]
	instr = each_row[14]
	lec_id = each_row[0]
	pairInstance = InstructorLectureIDPair(instr, lec_id)
	########################HOW DO I MAKE IT A LIST OF PAIR OF INSTANCES
	if !(course_id in dictionary.keys()):
		pairList = list()
	dictionary[course_id] = pairList.append(pairInstance)




''' write my own csv file'''
registrar_bruinwalk_similiarity_filename = os.path.join( \
        os_dir, '../ClassSchedulizer/lib/seeds/registrar_vs_bruinwalk_similiarity.csv')
registrar_bruinwalk_similiarity_file = open(registrar_bruinwalk_similiarity_filename, 'append')
registrar_bruinwalk_similiarity_writer = csv.writer(registrar_bruinwalk_similiarity_file, delimiter=',', \
        lineterminator='\r\n', quoting=csv.QUOTE_ALL)
registrar_bruinwalk_similiarity_writer.writerow(( \
        "lecture_id", "overall", "easiness", "workload", "clarity", "helpfulness"))





'''open/read bruinwalk csv file'''
class_rating_filename = os.path.join( \
       os_dir, '../ClassSchedulizer/lib/seeds/class_rating_data.csv')
class_rating_file = open(class_rating_filename, 'r')
class_rating_reader = csv.reader(class_rating_file, delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_ALL)
next(reader, None) # skip headers



'''write lecture id and 5 ratings to csv file'''
for row in class_rating_reader:
	if (row[0] in dictionary.keys()):
		for each_pair in dictionary[row[0]]:
			similiarityPercentageInstructor = fuzz.ratio(row[2], each_pair.instructor)
			if (similiarityPercentageInstructor > 75):
				l_id = each_pair.lecture_id
				overall = row[3]
				easiness =  row[4]
				workload = row[5]
				clarity = row[6]
				helpfulness = row[7]
				registrar_bruinwalk_similiarity_writer.writerow((l_id, overall, easiness, workload, clarity, helpfulness))









