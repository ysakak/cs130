from indexer import get_similarities_for_tuning
from test_similarity import get_rules, get_score
import copy
import sys

class Weight:
    def __init__(self, signal_min, signal_max, signal_incr):
        self.signal_min = signal_min
        self.signal_max = signal_max
        self.signal_incr = signal_incr
        self.current = signal_min

    def at_max(self):
        return abs(self.current - self.signal_max) < 0.01

    def reset(self):
        self.current = self.signal_min

    def increment(self):
        self.current += self.signal_incr

    def get_current(self):
        return self.current

class NGramWeight:
    def __init__(self, ngram_min, ngram_max):
        self.ngram_min = ngram_min
        self.ngram_max = ngram_max
        self.current_min = ngram_min
        self.current_max = ngram_min

    def at_max(self):
        return self.current_min == self.ngram_max and \
               self.current_max == self.ngram_max

    def reset(self):
        self.current_min = self.ngram_min
        self.current_max = self.ngram_min

    def increment(self):
        if self.current_min < self.ngram_max:
            self.current_min += 1
        else:
            self.current_max += 1
            self.current_min = self.ngram_min

    def get_current(self):
        return (self.current_min, self.current_max)

class Schema:
    def __init__(self, ngram_weight, idf_threshold_weight, title_similarity_weight, \
                 major_code_weight, course_level_weight, course_type_weight, \
                 course_level_min_weight, course_type_min_weight):
        self.ngram_weight = ngram_weight
        self.weights = [idf_threshold_weight, title_similarity_weight, major_code_weight, \
                        course_level_weight, course_type_weight, course_level_min_weight, \
                        course_type_min_weight]

    def at_max(self):
        if not self.ngram_weight.at_max():
            return False
        else:
            for i in range(len(self.weights)):
                if not self.weights[i].at_max():
                    return False

        return True

    def increment(self):
        for weight in reversed(self.weights):
            if weight.at_max():
                weight.reset()
                continue
            else:
                weight.increment()
                return

        self.ngram_weight.increment()

    def get_current(self):
        ngram_min, ngram_max = self.ngram_weight.get_current()
        weight_list = [weight.get_current() for weight in self.weights]
        return [ngram_min, ngram_max] + weight_list

def dummy_eval(similarities):
    total = 0.0
    for course_id, similarity_map in similarities.iteritems():
        for similar_course_id, score in similarity_map.iteritems():
            total += float(score)

    return total

def golden_set_eval(similarities):
    total_win_count, total_loss_count = get_score(similarities, get_rules())
    print "Total Win: %d, Total Loss: %d" % (total_win_count, total_loss_count)

    return float(total_win_count) * float(total_win_count) / (float(total_loss_count) + 1.0)

def eval(schema, eval_function):
    max_score = 0.0
    max_schema = copy.deepcopy(schema)

    while True:
        similarities = get_similarities_for_tuning(*schema.get_current())
        if similarities:
            score = eval_function(similarities)
            print schema.get_current()
            print score
            if score > max_score:
                max_schema = copy.deepcopy(schema)
                max_score = score

        if schema.at_max():
            break

        schema.increment()

        

    print "\nFinal Results:"
    print max_score
    print max_schema.get_current()

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')

    schema = Schema(NGramWeight(1, 1), Weight(1.0, 1.5, 0.1), Weight(0.1, 1.0, 0.1), \
                    Weight(1.0, 1.0, 1.0), Weight(1.0, 1.0, 1.0), Weight(1.0, 1.0, 1.0), \
                    Weight(1.0, 1.0, 1.0), Weight(1.0, 1.0, 1.0))

    eval(schema, golden_set_eval)
        




