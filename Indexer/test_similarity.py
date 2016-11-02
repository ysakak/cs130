import sys
import os
import csv

class Rule:
    def __init__(self, similar_course_id, operator, value):
        self.similar_course_id = similar_course_id
        self.operator = operator
        self.value = value
        # -1 = not applicable, 0 = false, 1 = true
        self.status = -1

    def test_rule(self, similarities):
        if self.operator == "=":
            most_similar_course_id = ""
            max_score = 0

            for similar_course_id, score in similarities.iteritems():
                if score > max_score:
                    most_similar_course_id = similar_course_id
                    max_score = score

            if most_similar_course_id == self.similar_course_id:
                self.status = 1
            else:
                self.status = 0
        elif self.operator == "<":
            if self.similar_course_id in similarities.keys() and self.value in similarities.keys():
                if similarities[self.similar_course_id] < similarities[self.value]:
                    self.status = 1
                else:
                    self.status = 0
            elif self.similar_course_id in similarities.keys():
                self.status = 0
            elif self.value in similarities.keys():
                self.status = 1
        elif self.operator == ">":
            if self.similar_course_id in similarities.keys() and self.value in similarities.keys():
                if similarities[self.similar_course_id] > similarities[self.value]:
                    self.status = 1
                else:
                    self.status = 0
            elif self.similar_course_id in similarities.keys():
                self.status = 1
            elif self.value in similarities.keys():
                self.status = 0

    def get_status(self):
        return self.status

    def to_csv(self):
        return "%s, %s, %s" % (self.similar_course_id, self.operator, self.value)

class Rules:
    def __init__(self, course_id, course_similarities):
        self.course_id = course_id
        self.course_similarities = course_similarities
        self.rules = list()
        self.win = 0
        self.loss = 0
        self.invalid = 0

    def add_rule(self, rule):
        self.rules.append(rule)

    def add_rules(self, rules):
        self.rules.extend(rules)

    def test_rules_and_output(self):
        results = list()

        for rule in self.rules:
            rule.test_rule(self.course_similarities)
            status = rule.get_status()
            results.append("%s, %s, %s" % (self.course_id, rule.to_csv().strip(), status))
            if status == 1: 
                self.win += 1
            elif status == 0:
                self.loss += 1
            else:
                self.invalid += 1

        return results

    def get_win_count(self):
        return self.win

    def get_loss_count(self):
        return self.loss

    def get_invalid_count(self):
        return self.invalid

def get_class_similarities(input_file):
    dir = os.path.dirname(__file__)
    class_similarity_filename = os.path.join(dir, '../ClassSchedulizer/db/' + input_file)
    file = open(class_similarity_filename, 'r')
    reader = csv.reader(file, delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_ALL)
    next(reader, None) # skip headers
    class_similarities = dict()

    for row in reader:
        course_id = row[0].strip()

        if course_id not in class_similarities.keys():
            class_similarities[course_id] = dict()

        class_similarities[course_id][row[1].strip()] = row[2].strip()

    file.close()
    return class_similarities

def get_rules():
    dir = os.path.dirname(__file__)
    rules_filename = os.path.join(dir, 'golden_set.txt')
    lines = tuple(open(rules_filename, 'r'))

    class_rules = dict()

    for line in lines:
        if line[0] == '#':
            continue

        cols = line.split(',')

        if len(cols) != 4:
            continue

        course_id = cols[0].strip()

        if course_id not in class_rules.keys():
            class_rules[course_id] = [Rule(cols[1].strip(), cols[2].strip(), cols[3].strip())]
        else:
            class_rules[course_id].append(Rule(cols[1].strip(), cols[2].strip(), cols[3].strip()))

    return class_rules

def test_rules_and_output():
    if len(sys.argv) < 2:
        print "indexer.py input_file"
        sys.exit(2)

    input_file = sys.argv[1]

    class_similarities = get_class_similarities(input_file)
    total_class_rules = get_rules()
    rule_outputs = list()
    total_win_count = 0
    total_loss_count = 0
    total_invalid_count = 0

    for course_id, rules in total_class_rules.iteritems():
        if course_id in class_similarities.keys():
            class_rules = Rules(course_id, class_similarities[course_id])
            class_rules.add_rules(rules)
            rule_outputs.extend(class_rules.test_rules_and_output())
            total_win_count += class_rules.get_win_count()
            total_loss_count += class_rules.get_loss_count()
            total_invalid_count += class_rules.get_invalid_count()
        else:
            total_invalid_count += len(rules)

    for rule_output in rule_outputs:
        print rule_output

    print "\n\nWin/Loss Ratio: %d/%d\tInvalid: %d" % (total_win_count, total_loss_count, total_invalid_count)

def get_score(class_similarities, total_class_rules):
    rule_outputs = list()
    total_win_count = 0
    total_loss_count = 0

    for course_id, rules in total_class_rules.iteritems():
        if course_id in class_similarities.keys():
            class_rules = Rules(course_id, class_similarities[course_id])
            class_rules.add_rules(rules)
            rule_outputs.extend(class_rules.test_rules_and_output())
            total_win_count += class_rules.get_win_count()
            total_loss_count += class_rules.get_loss_count()

    return (total_win_count, total_loss_count)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    test_rules_and_output()