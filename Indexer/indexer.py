from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import MySQLdb as mdb
from nltk.corpus import stopwords
import string
from multiprocessing.dummy import Pool as ThreadPool
import sys
import os
import csv
import re
import math
import numpy as np
import collections
from collections import Counter
import itertools
import copy

cached_stop_words = stopwords.words("english")

# taken from http://code.activestate.com/recipes/576694/
class OrderedSet(collections.MutableSet):

    def __init__(self, iterable=None):
        self.end = end = [] 
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

class LectureData:
    def __init__(self, course_id, course_type, major_code, title, description, level):
        self.course_id = course_id
        self.course_type = course_type
        self.major_code = major_code
        self.title = title
        self.description = description.split('.')
        self.level = level
        self.final_description = ""

    def __repr__(self):
        return "LectureData(%s, %s, %s)" % \
            (self.course_id, self.major_code, self.title)

    def __eq__(self, other):
        if isinstance(other, LectureData):
            return self.course_id == other.course_id
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.course_id)

class MajorData:
    def __init__(self, major_code, description_vector):
        self.major_code = major_code
        self.description_vector = description_vector
        self.cluster_id = -1

def get_lecture_details():
    dir = os.path.dirname(__file__)
    lecture_data_filename = os.path.join(dir, '../ClassSchedulizer/lib/seeds/independent_class_data.csv')
    file = open(lecture_data_filename, 'r')
    reader = csv.reader(file, delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_ALL)
    next(reader, None) # skip headers
    lecture_details = list()

    for row in reader:
        level = row[21]
        if level == "Lower Division" or level == "Upper Division":
            lecture_details.append(LectureData(row[3], row[1], row[6], row[4], row[8], level))

    file.close()
    return lecture_details

def generate_requisite_graphs():
    dir = os.path.dirname(__file__)
    requisite_filename = os.path.join(dir, '../ClassSchedulizer/lib/seeds/requisites.csv')
    file = open(requisite_filename, 'r')
    reader = csv.reader(file, delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_ALL)
    next(reader, None) # skip headers

    requisite_map = dict()
    requisite_for_map = dict()

    for row in reader:
        if row[0] in requisite_map.keys():
            requisite_map[row[0]].add(row[2])
        else:
            requisite_map[row[0]] = {row[2]}

        if row[3] != "":
            requisite_map[row[0]].add(row[3])

        if row[2] in requisite_for_map.keys():
            requisite_for_map[row[2]].add(row[0])
        else:
            requisite_for_map[row[2]] = {row[0]}

        if row[3] != "":
            if row[3] in requisite_for_map.keys():
                requisite_for_map[row[3]].add(row[0])
            else:
                requisite_for_map[row[3]] = {row[0]}

    return (requisite_map, requisite_for_map)

def get_all_requisites(course_id, requisite_map):
    if course_id not in requisite_map:
        return {}

    requisites_queue = OrderedSet(requisite_map[course_id])
    requisites = set(requisite_map[course_id])

    while len(requisites_queue) > 0:
        requisite = requisites_queue.pop()
        if requisite in requisite_map.keys():
            secondary_requisites = requisite_map[requisite]
            for secondary_requisite in secondary_requisites:
                if secondary_requisite not in requisites:
                    requisites.add(secondary_requisite)
                    requisites.add(secondary_requisite)

    return requisites

def get_average_idf(sentence, idf_lookup_table):
    table=string.maketrans(string.punctuation,' '*len(string.punctuation))

    tokens = sentence.lower().translate(table).split(' ')
    filtered_tokens = filter(lambda token: token not in cached_stop_words, tokens)
    tokens = re.sub(r"\s+", ' ', ' '.join(filtered_tokens)).strip().split(' ')
    total_idf = 0.0

    for token in tokens:
        if any(char.isdigit() for char in token):
            total_idf += idf_lookup_table['#']
        else:
            total_idf += idf_lookup_table[token]
        
    return total_idf / len(tokens)

def process_lecture_data(lecture_data, idf_lookup_table, idf_threshold):
    table=string.maketrans(string.punctuation,' '*len(string.punctuation))
    filtered_descriptions = list()

    for description in lecture_data.description:
        average_idf = get_average_idf(description, idf_lookup_table)
        if average_idf >= idf_threshold:
            filtered_descriptions.append(description)

    final_description = ' '.join(filtered_descriptions)
    tokens = final_description.lower().translate(table).split(' ')
    filtered_tokens = filter(lambda token: token not in cached_stop_words, tokens)
    lecture_data.final_description =  re.sub(r"\s+", ' ', ' '.join(filtered_tokens)).strip()

    title_tokens = lecture_data.title.lower().translate(table).split(' ')
    filtered_title_tokens = filter(lambda token: token not in cached_stop_words, title_tokens)
    lecture_data.title = re.sub(r"\s+", ' ', ' '.join(filtered_title_tokens)).strip()

    return lecture_data

def process_lecture_data_list(lecture_data_list, idf_lookup_table, idf_threshold):
    pool = ThreadPool(4)
    filtered_lecture_data_list = pool.map(lambda params: process_lecture_data(*params), itertools.izip(lecture_data_list, \
                                                                    itertools.repeat(idf_lookup_table), \
                                                                    itertools.repeat(idf_threshold)))
    pool.close()
    pool.join()

    return filtered_lecture_data_list

def generate_idf_lookup_table(lecture_data_list):
    table=string.maketrans(string.punctuation,' '*len(string.punctuation))
    corpus = list()
    lecture_count = 0

    for lecture_data in lecture_data_list:
        lecture_description_set = set()
        for description in lecture_data.description:
            tokens = description.lower().translate(table).split(' ')
            for i in range(len(tokens)):
                if any(char.isdigit() for char in tokens[i]):
                    tokens[i] = '#'

            filtered_tokens = filter(lambda token: token not in cached_stop_words, tokens)
            lecture_description_set |= set(re.sub(r"\s+", ' ', ' '.join(filtered_tokens)).strip().split(' '))
        corpus += list(lecture_description_set)
        lecture_count += 1

    counter = Counter(corpus)
    idf_lookup_table = dict()
    for token, count in counter.iteritems():
        idf_lookup_table[token] = math.log10(float(lecture_count) / float(count))

    return idf_lookup_table

def compute_similarities(data, min_n_gram, max_n_gram):
    tfidf_vectorizer = TfidfVectorizer(ngram_range=(min_n_gram, max_n_gram))
    tfidf_matrix_train = tfidf_vectorizer.fit_transform(data)
    return cosine_similarity(tfidf_matrix_train, tfidf_matrix_train)

def debug_similarities(similarities_matrix, id_lookup_table, title_lookup_table, \
                       similarity_name_list, similarity_matrix_list):
    requisite_map, requisite_for_map = generate_requisite_graphs()
    similarity_matrix_list_size = len(similarity_matrix_list)

    for i, row in enumerate(similarities_matrix):
        similarities = dict()
        for j, score in enumerate(row):
            if score != 1 and i != j:
                similarities[j] = score

        count = 0
        similarity_list = list()

        for key, value in sorted(similarities.iteritems(), key=lambda (k,v): (v,k), reverse=True):
            if value < 0.99999999 and value > 0.1 and check_if_valid_similarity(id_lookup_table[i], id_lookup_table[key], requisite_map, requisite_for_map):
                course_id = id_lookup_table[key]
                similarity_list.append((course_id + " " + title_lookup_table[course_id], value, i, key))
                count += 1
                if count == 5:
                    break

        if len(similarity_list) > 0:
            print "%s %s" % (id_lookup_table[i], title_lookup_table[id_lookup_table[i]])
            for similarity_data in similarity_list:
                print "\t%s %f" % (similarity_data[0], similarity_data[1])
                for k in range(similarity_matrix_list_size):
                    print "\t\t%s %f" % (similarity_name_list[k], similarity_matrix_list[k][similarity_data[2]][similarity_data[3]])

def output_similarities_to_csv(output_file, similarities_matrix, id_lookup_table):
    requisite_map, requisite_for_map = generate_requisite_graphs()
    os_dir = os.path.dirname(__file__)
    class_similarity_filename = os.path.join( \
        os_dir, '../ClassSchedulizer/lib/seeds/' + output_file)
    class_similarity_file = open(class_similarity_filename, 'w')
    class_similarity_writer = csv.writer(class_similarity_file, delimiter=',', \
        lineterminator='\r\n', quoting=csv.QUOTE_ALL)
    class_similarity_writer.writerow(("course_id", "similar_course_id", "score"))

    for i, row in enumerate(similarities_matrix):
        similarities = dict()
        course_id = id_lookup_table[i]

        for j, score in enumerate(row):
            similar_course_id = id_lookup_table[j]

            if score < 0.99 and score > 0.1 and \
                check_if_valid_similarity(course_id, similar_course_id,
                                          requisite_map, requisite_for_map):
                similarities[similar_course_id] = score

        count = 0

        for similar_course_id, score in sorted(similarities.iteritems(), key=lambda (k,v): (v,k), reverse=True):
            class_similarity_writer.writerow((course_id, similar_course_id, score))
            count += 1
            if count > 5:
                break

    class_similarity_file.close()

def normalization_function_add(input, weight = 1.0):
    return input + weight

def normalization_function_default(input, weight = 1.0):
    return input * weight

def normalization_function_sqrt(input, weight = 0.5):
    return math.pow(input, weight)

def combine_similarities(similarities_matrix_1, similarities_matrix_2, normalization_function, weight):
    similarities_matrix = copy.deepcopy(similarities_matrix_1)
    for i, row in enumerate(similarities_matrix_2):
        for j, score in enumerate(row):
            similarities_matrix[i][j] *= normalization_function(score, weight)

    return similarities_matrix

def check_if_valid_similarity(course_id, similar_course_id, requisite_map, requisite_for_map):
    requisites = []
    requisites_for = []

    if course_id in requisite_map.keys():
        requisites = requisite_map[course_id]
    if course_id in requisite_for_map.keys():
        requisites_for = requisite_for_map[course_id]

    if similar_course_id in requisites or similar_course_id in requisites_for:
        return False

    similar_class_requisites = []

    if similar_course_id in requisite_map.keys():
        similar_class_requisites = requisite_map[similar_course_id]

    return set(requisites).issuperset(set(similar_class_requisites))

def filter_similarity_map(similarities_matrix, id_lookup_table):
    requisite_map, requisite_for_map = generate_requisite_graphs()
    for i, row in enumerate(similarities_matrix):
        requisites = get_all_requisites(id_lookup_table[i], requisite_map)
        requisites_for = get_all_requisites(id_lookup_table[i], requisite_for_map)

        for j, score in enumerate(row):
            if i == j:
                similarities_matrix[i][j] = 0.0

            if not check_if_valid_similarity(id_lookup_table[i], id_lookup_table[j], requisite_map, requisite_for_map):
                similarities_matrix[i][j] = 0.0

            if score > 0.99:
                similarities_matrix[i][j] = 0.0



def generate_major_descriptions(lecture_data_list):
    major_to_description_map = dict()

    for i, lecture_data in enumerate(lecture_data_list):
        if lecture_data.major_code in major_to_description_map.keys():
            major_to_description_map[lecture_data.major_code] += " " + lecture_data.final_description
        else:
            major_to_description_map[lecture_data.major_code] = lecture_data.final_description

    return major_to_description_map

def get_major_code_similarity_lookup_table(lecture_data_list, id_lookup_table, ngram_min = 1, \
                                           ngram_max = 1):
    major_code_lookup_table = dict()
    descriptions = list()
    count = 0

    major_to_description_map = generate_major_descriptions(lecture_data_list)

    for major_code, description in major_to_description_map.iteritems():
        major_code_lookup_table[count] = major_code
        descriptions.append(description)
        count += 1

    description_similarities = np.matrix(compute_similarities(descriptions, ngram_min, ngram_max)) # n x n
    major_to_course_id_matrix = np.zeros((len(major_to_description_map.keys()), len(id_lookup_table))) # n x m

    course_id_to_index_map = {value: key for key, value in id_lookup_table.iteritems()}
    major_code_to_index_map = {value: key for key, value in major_code_lookup_table.iteritems()}

    for lecture_data in lecture_data_list:
        major_to_course_id_matrix[major_code_to_index_map[lecture_data.major_code]][course_id_to_index_map[lecture_data.course_id]] = 1

    return (major_to_course_id_matrix.transpose() * description_similarities * major_to_course_id_matrix).tolist()

# upperdiv -> lowerdiv = 0.5, same vice versa
def get_course_level_similarity_lookup_table(lecture_data_list, id_lookup_table, min_weight = 0.1):
    course_level_similarity_matrix = np.zeros((len(id_lookup_table), len(id_lookup_table)))
    course_id_to_index_map = {value: key for key, value in id_lookup_table.iteritems()}

    index_to_level_map = dict()

    for lecture_data in lecture_data_list:
        index_to_level_map[course_id_to_index_map[lecture_data.course_id]] = lecture_data.level

    for i in range(len(id_lookup_table)):
        for j in range(len(id_lookup_table)):
            if index_to_level_map[i] == index_to_level_map[j]:
                course_level_similarity_matrix[i][j] = 1.0
            else:
                course_level_similarity_matrix[i][j] = min_weight

    return course_level_similarity_matrix

def get_course_type_similarity_lookup_table(lecture_data_list, id_lookup_table, min_weight = 0.1):
    course_type_similarity_matrix = np.zeros((len(id_lookup_table), len(id_lookup_table)))
    course_id_to_index_map = {value: key for key, value in id_lookup_table.iteritems()}

    index_to_type_map = dict()

    for lecture_data in lecture_data_list:
        index_to_type_map[course_id_to_index_map[lecture_data.course_id]] = lecture_data.course_type

    for i in range(len(id_lookup_table)):
        for j in range(len(id_lookup_table)):
            if index_to_type_map[i] == index_to_type_map[j]:
                course_type_similarity_matrix[i][j] = 1.0
            else:
                course_type_similarity_matrix[i][j] = min_weight

    return course_type_similarity_matrix

def get_lecture_description_similarities(lecture_data_list, id_lookup_table, idf_threshold, ngram_min = 1, \
                                         ngram_max = 1):
    idf_lookup_table = generate_idf_lookup_table(lecture_data_list)
    lecture_data_set = process_lecture_data_list(set(lecture_data_list), idf_lookup_table, idf_threshold)

    title_lookup_table = dict()
    major_code_lookup_table = dict()
    titles = list()
    descriptions = list()

    for i, lecture_data in enumerate(lecture_data_set):
        major_code_lookup_table[i] = lecture_data.major_code
        title_lookup_table[lecture_data.course_id] = lecture_data.title
        titles.append(lecture_data.title)
        descriptions.append(lecture_data.final_description)

    
    return (compute_similarities(descriptions, ngram_min, ngram_max), compute_similarities(titles, ngram_min, ngram_max), \
            get_major_code_similarity_lookup_table(lecture_data_set, id_lookup_table))

def get_similarities():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print "indexer.py idf_threshold (output_file)"
        sys.exit(2)

    idf_threshold = float(sys.argv[1])

    if len(sys.argv) == 3:
        output_file = sys.argv[2]

    lecture_data_list = get_lecture_details()
    lecture_data_set = set(lecture_data_list)
    id_lookup_table = dict()
    title_lookup_table = dict()

    for i, lecture_data in enumerate(lecture_data_set):
        id_lookup_table[i] = lecture_data.course_id
        title_lookup_table[lecture_data.course_id] = lecture_data.title

    lecture_description_similarity, lecture_title_similarity,  major_code_similarity = \
        get_lecture_description_similarities(lecture_data_list, id_lookup_table, idf_threshold)
    level_similarity = get_course_level_similarity_lookup_table(lecture_data_set, id_lookup_table)
    course_type_similarity = get_course_type_similarity_lookup_table(lecture_data_set, id_lookup_table)

    total_similarity = combine_similarities(lecture_description_similarity, lecture_title_similarity, normalization_function_add, 1.0)
    total_similarity = combine_similarities(total_similarity, major_code_similarity, normalization_function_sqrt, 0.5)
    total_similarity = combine_similarities(total_similarity, level_similarity, normalization_function_default, 1.0)
    total_similarity = combine_similarities(total_similarity, course_type_similarity, normalization_function_default, 1.0)
    #total_similarity = filter_similarity_map(total_similarity.tolist(), id_lookup_table)

    similarity_name_list = ["lecture_description", "lecture_title", "major_code", "level", "course_type"]
    similarity_matrix_list = [lecture_description_similarity, lecture_title_similarity, major_code_similarity, \
                              level_similarity, course_type_similarity]
    
    if len(sys.argv) == 2:
        debug_similarities(total_similarity, id_lookup_table, title_lookup_table, \
                           similarity_name_list, similarity_matrix_list)
    elif len(sys.argv) == 3:
        output_similarities_to_csv(output_file, total_similarity, id_lookup_table)

def prepare_similarities_for_eval(similarities_matrix, id_lookup_table):
    requisite_map, requisite_for_map = generate_requisite_graphs()
    similarity_map = dict()
    for i, row in enumerate(similarities_matrix):
        similarities = dict()
        final_similarities = dict()
        course_id = id_lookup_table[i]

        for j, score in enumerate(row):
            similar_course_id = id_lookup_table[j]

            if score < 0.99 and score > 0.1 and \
               check_if_valid_similarity(course_id, similar_course_id,
                                         requisite_map, requisite_for_map):
                similarities[similar_course_id] = score

        count = 0

        for similar_course_id, score in sorted(similarities.iteritems(), key=lambda (k,v): (v,k), reverse=True):
            final_similarities[similar_course_id] = score
            count += 1
            if count > 5:
                break

        if len(final_similarities) > 0:
            similarity_map[course_id] = final_similarities

    return similarity_map

def get_similarities_for_tuning(ngram_min, ngram_max, idf_threshold, title_similarity_weight, major_code_weight, course_level_weight, \
                                course_type_weight, course_level_min_weight, course_type_min_weight):

    lecture_data_list = get_lecture_details()
    lecture_data_set = set(lecture_data_list)
    id_lookup_table = dict()

    for i, lecture_data in enumerate(lecture_data_set):
        id_lookup_table[i] = lecture_data.course_id

    lecture_description_similarity, lecture_title_similarity,  major_code_similarity = \
        get_lecture_description_similarities(lecture_data_list, id_lookup_table, idf_threshold)
    level_similarity = get_course_level_similarity_lookup_table(lecture_data_set, id_lookup_table, course_level_min_weight)
    course_type_similarity = get_course_type_similarity_lookup_table(lecture_data_set, id_lookup_table, course_type_min_weight)
    
    total_similarity = combine_similarities(lecture_description_similarity, lecture_title_similarity, normalization_function_add, title_similarity_weight)
    total_similarity = combine_similarities(total_similarity, major_code_similarity, normalization_function_sqrt, major_code_weight)
    total_similarity = combine_similarities(total_similarity, level_similarity, normalization_function_default, course_level_weight)
    total_similarity = combine_similarities(total_similarity, course_type_similarity, normalization_function_default, course_type_weight)
    #total_similarity = filter_similarity_map(total_similarity.tolist(), id_lookup_table)
    #debug_similarities(total_similarity, id_lookup_table, title_lookup_table)
    return prepare_similarities_for_eval(total_similarity, id_lookup_table)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    get_similarities()
