#!/usr/bin/python
"""Scrapes legacy.registrar.ucla.edu for lecture/discussion data."""
import itertools
import re
import requests
import sys
import MySQLdb as mdb
from lxml import html
from multiprocessing.dummy import Pool as ThreadPool

class SectionData:
    """ Stores data about a class that is shared among lectures and discussions"""
    def __init__(self, class_id, section, days, start, stop, building, room, url):
        self.class_id = class_id
        self.section = section
        self.days = days
        self.start = start
        self.stop = stop
        self.building = building
        self.room = room
        self.url = url

    def copy_init(self, section_data):
        self.class_id = section_data.class_id
        self.section = section_data.section
        self.days = section_data.days
        self.start = section_data.start
        self.stop = section_data.stop
        self.building = section_data.building
        self.room = section_data.room
        self.url = section_data.url

class LectureData(SectionData):
    def __init__(self, section_data):
        self.copy_init(section_data)

class DiscussionData(SectionData):
    def __init__(self, section_data, lecture_id):
        self.copy_init(section_data)
        self.lecture_id = lecture_id

class ClassData:
    def __init__(self, class_title, major, term, class_url):
        self.title = class_title
        self.major = major
        self.term = term
        self.url = class_url
        self.lectures = list()
        self.discussions = list()

    def __repr__(self):
        return "ClassData(%s)" % (self.title)

    def __eq__(self, other):
        if isinstance(other, ClassData):
            return self.title == other.title
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())

    def set_lectures(self, lectures):
        self.lectures = lectures

    def set_discussions(self, discussions):
        self.discussions = discussions

def get_page(url):
    page = None
    max_tries = 10
    page = None
    while page is None:
        try:
            page = requests.get(url)
        except Exception:
            print "Connection aborted... trying again"
            --max_tries
            if max_tries == 0:
                raise Exception('Connection aborted 10 times for ' + url)
            pass
    return page

def generate_lecture_url(srs, term):
    return "http://legacy.registrar.ucla.edu/schedule/subdet.aspx?srs=" + srs + \
           "&term=" + term + "&session="

def generate_class_description_url(termsel, subareasel, idxcrs):
    return "http://legacy.registrar.ucla.edu/schedule/detselect.aspx?termsel=" + termsel + \
           "&subareasel=" + subareasel + "&idxcrs=" + idxcrs

def generate_class_id_url(termsel, subareasel):
    return "http://legacy.registrar.ucla.edu/schedule/crsredir.aspx?termsel=" + termsel + \
           "&subareasel=" + subareasel

def get_class_id(url):
    match = re.compile('srs=(.*)&term')
    return match.search(url).group(1)

def get_if_exists(l, index):
    if len(l) <= index or index < 0:
        return ""
    else:
        return l[index]

def assign(l, index, value):
    if len(l) <= index:
        l.append(value)
    else:
        l[index] = value

    return l

def get_lectures_and_discussions(class_data):
    print "Getting lectures/discussions for " + class_data.title
    page = get_page(class_data.url)
    tree = html.fromstring(page.content)
    lecture_tables = tree.xpath('//table[starts-with(@id, "dgdLectureHeader")]')
    lecture_count = len(lecture_tables)
    if lecture_count == 0:
        return class_data

    urls = tree.xpath('//td[@class="dgdClassDataColumnIDNumber"]//a//@href')
    sections = tree.xpath('//td[@class="dgdClassDataSectionNumber"]//span//span//text() | ' \
                          '//td[@class="dgdClassDataSectionNumber"]//span//text()')
    days = tree.xpath('//td[@class="dgdClassDataDays"]//span//span//text() | ' \
                      '//td[@class="dgdClassDataDays"]//span//text()')
    start_times = tree.xpath('//td[@class="dgdClassDataTimeStart"]//span//span//text() | ' \
                             '//td[@class="dgdClassDataTimeStart"]//span//text()')
    end_times = tree.xpath('//td[@class="dgdClassDataTimeEnd"]//span//span//text() | ' \
                           '//td[@class="dgdClassDataTimeEnd"]//span//text()')
    buildings = tree.xpath('//td[@class="dgdClassDataBuilding"]//span//span//text() | ' \
                           '//td[@class="dgdClassDataBuilding"]//span//text()')
    rooms = tree.xpath('//td[@class="dgdClassDataRoom"]//span//span//text() | ' \
                       '//td[@class="dgdClassDataRoom"]//span//text()')
    ids = [(lambda url: get_class_id(url))(url) for url in urls]
    start_times = [(lambda time: time + "M")(time) for time in start_times]
    end_times = [(lambda time: time + "M")(time) for time in end_times]
    urls = [(lambda url: generate_lecture_url(lecture_id, class_data.term))(lecture_id) \
            for lecture_id in ids]

    section_data = list()

    max_length = max(max(len(ids), len(start_times)), len(buildings))
    for i in range(max_length):
        if i != 0:
            if get_if_exists(ids, i) == "":
                assign(ids, i, get_if_exists(ids, i-1))
            if get_if_exists(sections, i) == "":
                assign(sections, i, get_if_exists(sections, i-1))
            if get_if_exists(days, i) == "":
                assign(days, i, get_if_exists(days, i-1))
            if get_if_exists(start_times, i) == "":
                assign(start_times, i, get_if_exists(start_times, i-1))
            if get_if_exists(end_times, i) == "":
                assign(end_times, i, get_if_exists(end_times, i-1))
            if get_if_exists(buildings, i) == "":
                assign(buildings, i, get_if_exists(buildings, i-1))
            if get_if_exists(rooms, i) == "":
                assign(rooms, i, get_if_exists(rooms, i-1))
            if get_if_exists(urls, i) == "":
                assign(urls, i, get_if_exists(urls, i-1))


        section_data.append(SectionData(ids[i], sections[i], days[i], \
                                        get_if_exists(start_times, i), \
                                        get_if_exists(end_times, i), \
                                        get_if_exists(buildings, i), \
                                        get_if_exists(rooms, i), urls[i]))
    lecture_data = list()
    discussion_data = list()

    section_size = len(section_data) / lecture_count
    lecture_id = ""
    for i, section in enumerate(section_data):
        if i % section_size == 0:
            lecture_id = section.class_id
            lecture_data.append(LectureData(section))
        else:
            discussion_data.append(DiscussionData(section, lecture_id))

    class_data.set_lectures(lecture_data)
    class_data.set_discussions(discussion_data)

    return class_data

def get_major_class_details(termsel, subareasel):
    print "Getting classes for " + termsel + " " + subareasel
    page = get_page(generate_class_id_url(termsel, subareasel))
    tree = html.fromstring(page.content)
    class_ids = tree.xpath('//option//@value')
    class_titles = tree.xpath('//option/text()')
    class_data = list()

    for i, class_id in enumerate(class_ids):
        class_data.append(ClassData(class_titles[i], subareasel, termsel, \
                          generate_class_description_url(termsel, subareasel, class_id)))

    return class_data

def get_class_list(termsel):
    page = get_page("http://legacy.registrar.ucla.edu/schedule/schedulehome.aspx")
    tree = html.fromstring(page.content)
    majors = tree.xpath( \
        '//select[@id="ctl00_BodyContentPlaceHolder_SOCmain_lstSubjectArea"]//option//@value')

    class_data_list = list()

    reformatted_major_titles = list()

    for major in majors:
        reformatted_major_titles.append("+".join(major.split(' ')))

    pool = ThreadPool(4)
    class_data_list = pool.map(lambda args: get_major_class_details(*args), \
                               itertools.izip(itertools.repeat(termsel), \
                               reformatted_major_titles))
    pool.close()
    pool.join()

    return [class_data for major_class_data in class_data_list for class_data in major_class_data]

def get_total_class_list():
    class_data = list()

    for term in ['16W', '16S', '16F']:
        term_class_data = get_class_list(term)
        class_data.extend(term_class_data)
        break

    pool = ThreadPool(4)
    class_data_list = pool.map(get_lectures_and_discussions, class_data)
    pool.close()
    pool.join()

    return class_data_list

def write_to_db(class_data_list):
    db = mdb.connect('localhost', 'cs130', 'cs130')
    cursor = db.cursor()

    sql = 'CREATE DATABASE IF NOT EXISTS cs130'
    cursor.execute(sql)

    sql = 'USE cs130'
    cursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS lecture_data (
    id INT NOT NULL AUTO_INCREMENT,
    lecture_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    major VARCHAR(255) NOT NULL,
    term VARCHAR(255) NOT NULL,
    section VARCHAR(255) NOT NULL,
    days VARCHAR(255) NOT NULL,
    start VARCHAR(10) NOT NULL,
    stop VARCHAR(10) NOT NULL,
    building VARCHAR(255),
    room VARCHAR(255),
    url VARCHAR(255) NOT NULL,
    PRIMARY KEY(id)
    )'''
    cursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS discussion_data (
    id INT NOT NULL AUTO_INCREMENT,
    discussion_id INT NOT NULL,
    lecture_id INT NOT NULL,
    section VARCHAR(255) NOT NULL,
    days VARCHAR(255) NOT NULL,
    start VARCHAR(10) NOT NULL,
    stop VARCHAR(10) NOT NULL,
    building VARCHAR(255),
    room VARCHAR(255),
    url VARCHAR(255) NOT NULL,
    PRIMARY KEY(id)
    )'''
    cursor.execute(sql)


    for class_data in class_data_list:
        title = class_data.title
        major = " ".join(class_data.major.split("+"))
        term = class_data.term
        for lecture in class_data.lectures:
            sql = "INSERT INTO lecture_data(lecture_id, title, major, term, section, days, " \
                  "start, stop, building, room, url) VALUES (%s, %s, %s, %s, %s, %s, %s, " \
                  "%s, %s, %s, %s)"
            cursor.execute(sql, (lecture.class_id, title, major, term, lecture.section, \
                                 lecture.days, lecture.start, \
                                 lecture.stop, lecture.building, \
                                 lecture.room, lecture.url))
        for discussion in class_data.discussions:
            sql = "INSERT INTO discussion_data(discussion_id, lecture_id, section, days, " \
                  "start, stop, building, room, url) VALUES (%s, %s, %s, %s, %s, " \
                  "%s, %s, %s, %s)"
            cursor.execute(sql, (discussion.class_id, discussion.lecture_id, discussion.section, \
                                 discussion.days, discussion.start, discussion.stop, \
                                 discussion.building, discussion.room, discussion.url))
    try:
        db.commit()
    except:
        print "Write to db failed"
        db.rollback()
    db.close()
    
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    write_to_db(get_total_class_list())
