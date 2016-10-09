import MySQLdb as mdb
from nltk.corpus import stopwords
import string
from multiprocessing.dummy import Pool as ThreadPool
import sys

cached_stop_words = stopwords.words("english")

class LectureData:
    def __init__(self, lecture_id, title, description):
        self.lecture_id = lecture_id
        self.title = title
        self.description = description

def get_lecture_descriptions():
    db = mdb.connect('localhost', 'cs130', 'cs130')
    cursor = db.cursor()
    sql = 'USE cs130'
    cursor.execute(sql)
    sql = 'SELECT id, title, description FROM lecture_details'
    cursor.execute(sql)
    lecture_data_list = list()

    for row in cursor.fetchall():
        lecture_data_list.append(LectureData(row[0], row[1], row[2]))

    db.close()
    return lecture_data_list

def process_lecture_data(lecture_data):
    title_tokens = ''.join(c for c in lecture_data.title.split('-')[1].lower() \
                           if c not in string.punctuation).split(' ')
    description_tokens = ''.join(c for c in lecture_data.description.lower() \
                                 if c not in string.punctuation).split(' ')
    filtered_title_tokens = filter(lambda token: token not in cached_stop_words, title_tokens)
    filtered_description_tokens = filter(lambda token: token not in \
                                         cached_stop_words, description_tokens)

    lecture_data.title = ' '.join(filtered_title_tokens)
    lecture_data.description = ' '.join(filtered_description_tokens)

    return lecture_data

def process_lecture_data_list(lecture_data_list):
    pool = ThreadPool(4)
    filtered_lecture_data_list = pool.map(process_lecture_data, lecture_data_list)
    pool.close()
    pool.join()

    return filtered_lecture_data_list

def get_lfiltered_lecture_data_and_write_to_db():
    filtered_lecture_data_list = process_lecture_data_list(get_lecture_descriptions())
    db = mdb.connect('localhost', 'cs130', 'cs130')
    cursor = db.cursor()

    sql = 'USE cs130'
    cursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS filtered_lecture_data (
    id INT NOT NULL,
    title VARCHAR(255),
    description TEXT,
    PRIMARY KEY(id)
    )'''
    cursor.execute(sql)

    for filtered_lecture_data in filtered_lecture_data_list:
        sql = "INSERT INTO filtered_lecture_data(id, title, description) VALUES (%s, %s, %s)"
        cursor.execute(sql, (filtered_lecture_data.lecture_id, filtered_lecture_data.title, \
                             filtered_lecture_data.description))
        try:
            db.commit()
        except:
            print "Write to db failed"
            db.rollback()

    db.close()

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    get_lfiltered_lecture_data_and_write_to_db()
