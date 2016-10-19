''' Scraper that scrapes legacy.registrar.ucla.edu and sa.ucla.edu for classes. '''

import csv
import os
from multiprocessing.dummy import Pool as ThreadPool
import re
import string
import sys
import requests
from lxml import html

class Requisite:
    def __init__(self, operator, course_title_1, course_title_2):
        self.operator = operator
        self.course_title_1 = course_title_1
        self.course_title_2 = course_title_2

    def __repr__(self):
        return "Requisite(%s, %s, %s)" % \
            (operator, course_title_1, course_title_2)

''' Stores the data shared between independent and dependent classes. '''
class ClassData:
    def __init__(self, class_id, class_type, section, url):
        self.class_id = class_id
        self.class_type = class_type
        self.section = section
        self.url = url

        self.days = ""
        self.start_time = ""
        self.end_time = ""
        self.location = ""
        self.instructor = ""

''' Stores the data for an independent class. '''
class IndependentClassData(ClassData):
    def __init__(self, class_id, class_type, section, url):
        ClassData.__init__(self, class_id, class_type, section, url)

        self.final_examination_date = ""
        self.final_examination_day = ""
        self.final_examination_time = ""

''' Stores the data for a dependent class. '''
class DependentClassData(ClassData):
    def __init__(self, class_id, class_type, section, url):
        ClassData.__init__(self, class_id, class_type, section, url)
        self.independent_class_id = self.get_independent_class_id()

    ''' Converts a char to its integer representation.  Ex. "A" -> 1. '''
    def get_section_char_int(self):
        char_array = [c for c in self.section if not c.isdigit()]
        if len(char_array) == 1:
            return ord(char_array[0]) - 64

        return (ord(char_array[0]) - 64) * 26 + (ord(char_array[1]) - 64)

    ''' Retruns an int that represents the dependent class number for an
        independent class. '''
    def get_independent_class_id(self):
        return str(int(self.class_id) - self.get_section_char_int())

''' Stores the data for a course.  A course can have multiple (in)dependent classes. '''
class CourseData:
    def __init__(self, course_id, title, url):
        self.course_id = course_id
        self.title = title
        self.url = url
        self.description = ""
        self.units = ""
        self.grade_type = ""
        self.restrictions = ""
        self.impacted_class = ""
        self.level = ""
        self.text_book_url = ""

        self.independent_class_data = list()
        self.dependent_class_data = list()
        self.requisites = list()
        self.ge_categories = list()

    ''' Returns true if a section is a independent class. '''
    def is_independent_class(self, section):
        for c in section:
            if not c.isdigit():
                return False
        return True

    ''' Checks if a class is independent/dependent, and adds the class accordingly. '''
    def add_class(self, class_id, class_type, section, url):
        if self.is_independent_class(section):
            self.independent_class_data.append(IndependentClassData(class_id, class_type, \
                                                                    section, url))
        else:
            self.dependent_class_data.append(DependentClassData(class_id, class_type, \
                                                                section, url))

''' Stores the data for a major.  A major can have multiple courses. '''
class MajorData:
    def __init__(self, term, major, major_code, url):
        self.term = term
        self.major = major
        self.major_code = major_code
        self.url = url

        self.course_data = list()

''' Returns the page for a given url. Retries up to 10 times to retrieve the page. '''
def get_page(url):
    page = None
    max_tries = 10
    page = None
    while page is None:
        try:
            page = requests.get(url)
        except Exception:
            print "Connection aborted... trying again"
            max_tries -= 1
            if max_tries == 0:
                raise Exception('Connection aborted 10 times for ' + url)
    return page

''' Extracts the class id from a url. '''
def get_class_id(url):
    match = re.compile('srs=(.*)&term')
    return match.search(url).group(1)

''' Wrapper function for list retrieval. Returns empty string if the index is 
    out of range.  '''
def get_if_exists(l, index):
    if len(l) <= index or index < 0:
        return ""
    else:
        return l[index]

''' Wrapper function for list insertion. Appends to the end of the list if
    the index is out of range. '''
def assign(l, index, value):
    if len(l) <= index:
        l.append(value)
    else:
        l[index] = value

    return l

def format_for_url(subareasel):
    return subareasel.strip().replace(' ', '+').replace('&', '%26')

''' Extracts the numbers from class ids. '''
def generate_class_number(section):
    total = string.maketrans('', '')
    return int(section.translate(total, total.translate(total, string.digits)))

def generate_section_url(term, major, crs_catlg_no, class_id, class_no):
    return "https://sa.ucla.edu/ro/Public/SOC/Results/ClassDetail?term_cd=" + term + \
           "&subj_area_cd=" + format_for_url(major) + "&crs_catlg_no=" + \
           crs_catlg_no.replace(' ', '+') + "&class_id=" + class_id + "&class_no=%20" + \
           ("%03d" % generate_class_number(class_no))

def generate_course_description_url(termsel, subareasel, idxcrs):
    return "http://legacy.registrar.ucla.edu/schedule/detselect.aspx?termsel=" + termsel + \
           "&subareasel=" + format_for_url(subareasel) + "&idxcrs=" + idxcrs

def generate_major_url(termsel, subareasel):
    return "http://legacy.registrar.ucla.edu/schedule/crsredir.aspx?termsel=" + termsel + \
           "&subareasel=" + format_for_url(subareasel)

''' Returns the list of all majors for a term. '''
def get_major_list(term):
    page = get_page("http://legacy.registrar.ucla.edu/schedule/schedulehome.aspx")
    tree = html.fromstring(page.content)
    major_codes = tree.xpath( \
        '//select[@id="ctl00_BodyContentPlaceHolder_SOCmain_lstSubjectArea"]//option//@value')

    major_titles = tree.xpath( \
        '//select[@id="ctl00_BodyContentPlaceHolder_SOCmain_lstSubjectArea"]//option//text()')

    major_list = list()

    for i in range(len(major_titles)):
        major_list.append(MajorData(term, major_titles[i], major_codes[i], \
                                    generate_major_url(term, major_codes[i])))

    return major_list

''' Gets a list of courses offered by a major for a specific term. '''
def get_major_course_list(major_data):
    page = get_page(major_data.url)
    tree = html.fromstring(page.content)
    course_ids = tree.xpath('//option//@value')
    course_titles = tree.xpath('//option//text()')
    major = get_if_exists(tree.xpath('//span[@class="heading2green"]//text()'), 0)

    if major != "":
        major_data.major = major

    print "Getting courses for " + major_data.major

    for i in range(len(course_ids)):
        course_id = course_ids[i].strip()
        course_title = course_titles[i].strip()

        major_data.course_data.append( \
            CourseData(course_id, course_title, \
                       generate_course_description_url(major_data.term, major_data.major_code, \
                                                       course_id)))

''' Gets a list of lectures, discussions, etc.. for a major. '''
def get_course_data(major_data):
    term = major_data.term
    major_code = major_data.major_code

    print "Getting course data for " + major_data.major
    for course_data in major_data.course_data:
        course_id = course_data.course_id

        page = get_page(course_data.url)
        tree = html.fromstring(page.content)
        lecture_tables = tree.xpath('//table[starts-with(@id, "dgdLectureHeader")]')
        lecture_count = len(lecture_tables)
        if lecture_count == 0:
            return major_data

        urls = tree.xpath('//td[@class="dgdClassDataColumnIDNumber"]//a//@href')
        sections = tree.xpath('//td[@class="dgdClassDataSectionNumber"]//span//text()')
        types = tree.xpath('//td[@class="dgdClassDataActType"]//span//text()')

        ids = [(lambda url: get_class_id(url))(url) for url in urls]
        if len(urls) != len(sections) or len(urls) != len(types):
            print "incorrect data format: " + course_data.url
        for i in range(len(ids)):
            course_data.add_class(ids[i], types[i], sections[i], \
                generate_section_url(term, major_code, course_id, \
                                     ids[i], sections[i]))

        course_title_tokens = course_data.title.strip().split('-', 1)
        course_data.course_id = course_title_tokens[0].strip()
        course_data.title = course_title_tokens[1].strip()

def get_additional_course_data(course_data, url):
    page = get_page(url.strip())
    tree = html.fromstring(page.content)

    course_data.units = get_if_exists(tree.xpath( \
        '//div[@id="enrl_mtng_info"]//div[2]//div[@class="span6"]//text()'), 0)

    course_description = get_if_exists(tree.xpath('//div[@id="section"]//p[2]//text()'), 0)
    class_description = get_if_exists(tree.xpath('//div[@id="section"]//p[4]//text()'), 0)

    if course_description != "None":
        course_data.description += course_description
    if course_description != "None" and class_description != "None":
        course_data.description += " "
    if class_description != "None":
        course_data.description += class_description

    course_data.grade_type = get_if_exists( \
        tree.xpath('//div[@id="enrollment_info"]//div[2]//div[@class="span1"]//p//text()'), 0)
    course_data.restrictions = get_if_exists( \
        tree.xpath('//div[@id="enrollment_info"]//div[2]//div[@class="span2"]//p//text()'), 1)
    course_data.impacted_class = get_if_exists( \
        tree.xpath('//div[@id="enrollment_info"]//div[2]//div[@class="span3"]//p//text()'), 0)
    course_data.level = get_if_exists(tree.xpath( \
        '//div[@id="enrollment_info"]//div[2]//div[@class="span5"]//p//text()'), 0)
    course_data.text_book_url = get_if_exists(tree.xpath( \
        '//div[@id="textbooks"]//a//@href'), 0)

    requisites = tree.xpath('//div[@id="course_requisites"]//div[@class="overflow-autoScroll"]' \
                            '//a[@class="popover-right"]//text()')
    
    tmp_class_title_store = ""
    prev_was_or = False

    for requisite in requisites:
        requisite = re.sub('[()]', '', requisite).strip()
        if requisite.endswith(" and"):
            if prev_was_or:
                course_data.requisites.append(Requisite("OR", tmp_class_title_store, \
                                                        requisite[:-4].strip()))
            else:
                course_data.requisites.append(Requisite("AND", requisite[:-4].strip(), ""))
            prev_was_or = False
            tmp_class_title_store = ""
        elif requisite.endswith(" or"):
            if prev_was_or:
                course_data.requisites.append(Requisite("OR", tmp_class_title_store, \
                                                        requisite[:-3].strip()))
                tmp_class_title_store = requisite[:-3].strip()
            else:
                tmp_class_title_store = requisite[:-3].strip()
            prev_was_or = True
        else:
            if prev_was_or:
                course_data.requisites.append(Requisite("OR", tmp_class_title_store, \
                                                        requisite.strip()))
            else:
                course_data.requisites.append(Requisite("AND", requisite.strip(), ""))
            prev_was_or = False
            tmp_class_title_store = ""

    ge_categories = tree.xpath( \
        '//p[@class="section_data GE_subsection_data breakLongText"]//text()')
    for ge_category in ge_categories:
        course_data.ge_categories.append(ge_category.strip())

''' Gets the data for a independent class(lectures, discussions). '''
def get_independent_class_data(independent_class_data):
    page = get_page(independent_class_data.url.strip())
    tree = html.fromstring(page.content)

    independent_class_data.days = get_if_exists( \
        tree.xpath('//div[@id="enrl_mtng_info"]//div[2]//div[@class="span3"]//a//@data-content'), 0)
    independent_class_data.location = get_if_exists( \
        tree.xpath('//div[@id="enrl_mtng_info"]//div[2]//div[@class="span5"]//a//@data-content'), 0)
    times_str = get_if_exists(tree.xpath( \
        '//div[@id="enrl_mtng_info"]//div[2]//div[@class="span4"]//text()'), 0)
    if times_str != "":
        times = times_str.split('-')

        if len(times) == 2:
            independent_class_data.start_time = times[0]
            independent_class_data.end_time = times[1]
        else:
            independent_class_data.start_time = times[0]
            independent_class_data.end_time = times[0]

    independent_class_data.instructor = get_if_exists(tree.xpath( \
        '//div[@id="enrl_mtng_info"]//div[2]//div[@class="span7"]//text()'), 0)

    independent_class_data.final_examination_date = get_if_exists( \
        tree.xpath('//div[@id="final_exam_info"]//div[1]//div[2]//div[@class="span1"]//text()'), 0)
    independent_class_data.final_examination_day = get_if_exists( \
        tree.xpath('//div[@id="final_exam_info"]//div[1]//div[2]//div[@class="span2"]//text()'), 0)
    independent_class_data.final_examination_time = get_if_exists( \
        tree.xpath('//div[@id="final_exam_info"]//div[1]//div[2]//div[@class="span3"]//text()'), 0)

''' Gets the data for a independent class(discussions, labs, ..). '''
def get_dependent_class_data(dependent_class_data):
    page = get_page(dependent_class_data.url)
    tree = html.fromstring(page.content)

    dependent_class_data.days = get_if_exists( \
        tree.xpath('//div[@id="enrl_mtng_info"]//div[2]//div[@class="span3"]//a//@data-content'), 0)
    dependent_class_data.location = get_if_exists( \
        tree.xpath('//div[@id="enrl_mtng_info"]//div[2]//div[@class="span5"]//a//@data-content'), 0)
    times_str = get_if_exists( \
        tree.xpath('//div[@id="enrl_mtng_info"]//div[2]//div[@class="span4"]//text()'), 0)
    if times_str != "":
        times = times_str.split('-')

        if len(times) == 2:
            dependent_class_data.start_time = times[0]
            dependent_class_data.end_time = times[1]
        else:
            dependent_class_data.start_time = times[0]
            dependent_class_data.end_time = times[0]

    dependent_class_data.instructor = get_if_exists( \
        tree.xpath('//div[@id="enrl_mtng_info"]//div[2]//div[@class="span7"]//text()'), 0)

''' Gets the data for (in)dependent classes. '''
def get_class_data(major_data):
    print "Getting class data for " + major_data.major
    for course_data in major_data.course_data:
        processed_additonal_data = False

        for independent_class_data in course_data.independent_class_data:
            if not processed_additonal_data:
                get_additional_course_data(course_data, independent_class_data.url)
                processed_additonal_data = True
            get_independent_class_data(independent_class_data)
        for dependent_class_data in course_data.dependent_class_data:
            get_dependent_class_data(dependent_class_data)

''' Writes the class data to csv files. '''
def write_to_csv(major_data_list):
    os_dir = os.path.dirname(__file__)
    independent_classes_filename = os.path.join( \
        os_dir, '../ClassSchedulizer/db/independent_class_data.csv')
    independent_classes_file = open(independent_classes_filename, 'w')
    independent_classes_writer = csv.writer(independent_classes_file, delimiter=',', \
        lineterminator='\r\n', quoting=csv.QUOTE_ALL)
    independent_classes_writer.writerow(( \
        "lecture_id", "class_type", "section", "course_id", "title", "major", \
        "major_code", "term", "description", "days", "start_time", "end_time", "location", \
        "units", "instructor", "final_examination_date", "final_examination_day", \
        "final_examination_time", "grade_type", "restrictions", "impacted_class", \
        "level", "text_book_url", "url"))

    dependent_classes_filename = os.path.join( \
        os_dir, '../ClassSchedulizer/db/dependent_class_data.csv')
    dependent_classes_file = open(dependent_classes_filename, 'w')
    dependent_classes_writer = csv.writer(dependent_classes_file, delimiter=',', \
        lineterminator='\r\n', quoting=csv.QUOTE_ALL)
    dependent_classes_writer.writerow(( \
        "class_id", "lecture_id", "class_type", "section", "course_id", \
        "title", "major", "major_code", "term", "days", "start_time", "end_time", \
        "location", "instructor", "url"))

    requisites_filename = os.path.join(os_dir, '../ClassSchedulizer/db/requisites.csv')
    requisites_file = open(requisites_filename, 'w')
    requisites_writer = csv.writer(requisites_file, delimiter=',', \
        lineterminator='\r\n', quoting=csv.QUOTE_ALL)
    requisites_writer.writerow(("course_id", "operator", "requisite_course_id_1", \
                                "requisite_course_id_2"))

    ge_filename = os.path.join(os_dir, '../ClassSchedulizer/db/ge_categories.csv')
    ge_file = open(ge_filename, 'w')
    ge_writer = csv.writer(ge_file, delimiter=',', lineterminator='\r\n', \
        quoting=csv.QUOTE_ALL)
    ge_writer.writerow(("course_id", "foundation", "category"))
    major_code_map = dict()
    requisites = set()

    for major_data in major_data_list:
        print "Writing data for " + major_data.major + " to file."
        term = major_data.term
        major = major_data.major
        major_code = major_data.major_code
        major_code_map[major] = major_code

        for course_data in major_data.course_data:
            course_id = course_data.course_id
            title = course_data.title
            description = course_data.description
            units = course_data.units
            grade_type = course_data.grade_type
            restrictions = course_data.restrictions
            impacted_class = course_data.impacted_class
            level = course_data.level
            text_book_url = course_data.text_book_url

            for independent_class_data in course_data.independent_class_data:
                lecture_id = independent_class_data.class_id
                independent_classes_writer.writerow((lecture_id, \
                    independent_class_data.class_type, independent_class_data.section, \
                    course_id, title, major, major_code, term, description, \
                    independent_class_data.days, independent_class_data.start_time, \
                    independent_class_data.end_time, independent_class_data.location, \
                    units, independent_class_data.instructor, \
                    independent_class_data.final_examination_date, \
                    independent_class_data.final_examination_day, \
                    independent_class_data.final_examination_time, \
                    grade_type, restrictions, impacted_class, level, text_book_url, \
                    independent_class_data.url))

            for dependent_class_data in course_data.dependent_class_data:
                dependent_classes_writer.writerow((dependent_class_data.class_id, \
                    dependent_class_data.independent_class_id, dependent_class_data.class_type, \
                    dependent_class_data.section, course_id, title, major, major_code, \
                    term, dependent_class_data.days, dependent_class_data.start_time, \
                    dependent_class_data.end_time, dependent_class_data.location, \
                    dependent_class_data.instructor, dependent_class_data.url))

            for requisite in course_data.requisites:
                requisites.add((course_id, requisite))

            for ge_category in course_data.ge_categories:
                ge_category_tokens = ge_category.split('-')
                if len(ge_category_tokens) == 2:
                    ge_writer.writerow((course_id, ge_category_tokens[0].strip(),
                                        ge_category_tokens[1].strip()))

    for total_course_id, requisite in requisites:
        course_title_1_tokens = requisite.course_title_1.rsplit(' ', 1)
        course_title_1 = course_title_1_tokens[0].strip()
        course_title_id_1 = course_title_1_tokens[1].strip()
        if course_title_1 in major_code_map.keys():
            course_title_1 = major_code_map[course_title_1]

        if requisite.operator == "OR":
            course_title_2_tokens = requisite.course_title_2.rsplit(' ', 1)
            course_title_2 = course_title_2_tokens[0].strip()
            course_title_id_2 = course_title_2_tokens[1].strip()
            if course_title_2 in major_code_map.keys():
                course_title_2 = major_code_map[course_title_2]

            requisites_writer.writerow((total_course_id, requisite.operator, \
                                        course_title_1 + " " + course_title_id_1, \
                                        course_title_2 + " " + course_title_id_2))
        else:
            requisites_writer.writerow((total_course_id, requisite.operator, \
                                        course_title_1 + " " + course_title_id_1, \
                                        ""))
    independent_classes_file.close()
    dependent_classes_file.close()
    requisites_file.close()
    ge_file.close()

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')

    majors = get_major_list('16F')

    course_list_pool = ThreadPool(4)
    course_list_pool.map(get_major_course_list, majors)
    course_list_pool.close()
    course_list_pool.join()

    course_data_pool = ThreadPool(4)
    course_data_pool.map(get_course_data, majors)
    course_data_pool.close()
    course_data_pool.join()

    class_data_pool = ThreadPool(4)
    class_data_pool.map(get_class_data, majors)
    class_data_pool.close()
    class_data_pool.join()
    write_to_csv(majors)
