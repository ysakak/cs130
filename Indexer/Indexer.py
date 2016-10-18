from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import MySQLdb as mdb
from nltk.corpus import stopwords
import string
from multiprocessing.dummy import Pool as ThreadPool
import sys
import os
import csv

cached_stop_words = stopwords.words("english")

class LectureData:
    def __init__(self, lecture_id, major_code, title_number, title, description):
        self.lecture_id = lecture_id
        self.major_code = major_code
        self.title_number = title_number
        self.title = title
        self.description = description

def get_lecture_details():
    dir = os.path.dirname(__file__)
    lecture_data_filename = os.path.join(dir, '../ClassSchedulizer/db/lecture_details.csv')
    file = open(lecture_data_filename, 'r')
    reader = csv.reader(file, delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_ALL)
    next(reader, None) # skip headers
    lecture_details = set()

    for row in reader:
        title_number = ''.join(c for c in row[1] if c not in string.ascii_letters)
        if title_number != "" and int(title_number) < 200:
            lecture_details.add(LectureData(row[0], row[4], row[1], row[2], row[5]))

    file.close()
    return lecture_details

def process_lecture_data(lecture_data):
    title_tokens = ''.join(c for c in lecture_data.title.lower() \
                                 if c not in string.punctuation).split(' ')
    description_tokens = ''.join(c for c in lecture_data.description.lower() \
                                 if c not in string.punctuation).split(' ')
    filtered_title_tokens = filter(lambda token: token not in cached_stop_words, title_tokens)
    filtered_description_tokens = filter(lambda token: token not in \
                                         cached_stop_words, description_tokens)
    filtered_description_tokens = filter(lambda token: len(token) > 2, filtered_description_tokens)
    lecture_data.title = ' '.join(filtered_title_tokens)
    lecture_data.description = ' '.join(filtered_description_tokens)
    if len(filtered_description_tokens) < 15:
        lecture_data.description = ""

    return lecture_data

def process_lecture_data_list(lecture_data_list):
    pool = ThreadPool(4)
    filtered_lecture_data_list = pool.map(process_lecture_data, lecture_data_list)
    pool.close()
    pool.join()

    return filtered_lecture_data_list

def compute_similarities(data):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix_train = tfidf_vectorizer.fit_transform(data)
    return cosine_similarity(tfidf_matrix_train, tfidf_matrix_train)

def debug_similarities(similarities_matrix, id_lookup_table):
    for i, row in enumerate(similarities_matrix):
        similarities = dict()
        for j, score in enumerate(row):
            if score != 1 and i != j:
                similarities[id_lookup_table[j]] = score
        print id_lookup_table[i]
        count = 0
        for key, value in sorted(similarities.iteritems(), key=lambda (k,v): (v,k), reverse=True):
            if value > 0.3:
                print "\t%s %f" %(key, value)
                count += 1
                if count == 10:
                    break

def combine_similarities(similarities_matrix_1, similarities_matrix_2):
    for i, row in enumerate(similarities_matrix_1):
        for j, score in enumerate(row):
            if score != 1 and similarities_matrix_2[i][j] != 1:
                similarities_matrix_1[i][j] = (score * 0.25 + similarities_matrix_2[i][j])
    return similarities_matrix_1

def get_similarities():
    lecture_data_list = process_lecture_data_list(get_lecture_details())
    id_lookup_table = dict()
    titles = list()
    descriptions = list()

    for i, lecture_data in enumerate(lecture_data_list):
        id_lookup_table[i] = lecture_data.major_code + " " + lecture_data.title_number + " " + lecture_data.title
        titles.append(lecture_data.title)
        descriptions.append(lecture_data.description)

    title_similarities = compute_similarities(titles)
    description_similarities = compute_similarities(descriptions)
    debug_similarities(combine_similarities(title_similarities, description_similarities), \
                       id_lookup_table)
    
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    get_similarities()