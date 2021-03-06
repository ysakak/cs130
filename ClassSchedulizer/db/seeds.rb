# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)

require 'csv'
require 'time'
require 'date'

csv_independent_class = File.read(Rails.root.join('lib', 'seeds', 'independent_class_data.csv'))
csv = CSV.parse(csv_independent_class, :headers => true, :encoding => 'UTF-8')
class_data_title_set = Set.new

csv.each do |row|
	t = IndependentClassData.new
	t.lecture_id = row['lecture_id']
	t.class_type = row['class_type']
	t.section = row['section']
	t.course_id = row['course_id']
	t.title = row['title']
	t.major = row['major']
	t.major_code = row['major_code']
	t.term = row['term']
	t.description = row['description']
	t.days = row['days']

	if row['start_time'].nil? || row['start_time'].empty? || row['start_time'] == "To be arranged"
		t.start_time = nil
	elsif row['start_time'].include? ":"
		t.start_time = Time.strptime(row['start_time'] + " UTC", '%l:%M%P %Z')
	else
		t.start_time = Time.strptime(row['start_time'] + " UTC", '%l%P %Z')
	end

	if row['end_time'].nil? || row['end_time'].empty? || row['end_time'] == "To be arranged"
		t.end_time = nil
	elsif row['end_time'].include? ":"
		t.end_time = Time.strptime(row['end_time'] + " UTC", '%l:%M%P %Z')
	else
		t.end_time = Time.strptime(row['end_time'] + " UTC", '%l%P %Z')
	end

	t.location = row['location']
	t.units = row['units']
	t.instructor = row['instructor']
	if row['final_examination_date'].eql? "None listed"
		t.final_examination_date = nil
	else
		t.final_examination_date = Date.strptime(row['final_examination_date'], '%b %d, %Y')
	end
	t.final_examination_day = row['final_examination_day']
	t.final_examination_time = row['final_examination_time']
	t.grade_type = row['grade_type']
	t.restrictions = row['restrictions']
	t.impacted_class = row['impacted_class']
	t.level = row['level']
	t.text_book_url = row['text_book_url']
	t.url = row['url']

	t.save
	puts "#{t.title} saved"

	if class_data_title_set.exclude?(row['course_id'])
		s = ClassData.new
		s.course_id = row['course_id']
		s.title = row['title']
		s.major = row['major']
		s.major_code = row['major_code']
		s.term = row['term']
		s.description = row['description']
		s.units = row['units']
		s.grade_type = row['grade_type']
		s.restrictions = row['restrictions']
		s.impacted_class = row['impacted_class']
		s.level = row['level']
		class_data_title_set << row['course_id']
		s.save
	end
end

csv_dependent_class = File.read(Rails.root.join('lib', 'seeds', 'dependent_class_data.csv'))
csv = CSV.parse(csv_dependent_class, :headers => true, :encoding => 'UTF-8')
csv.each do |row|
	t = DependentClassData.new
	t.class_id = row['class_id']
	t.lecture_id = row['lecture_id']
	t.class_type = row['class_type']
	t.section = row['section']
	t.course_id = row['course_id']
	t.title = row['title']
	t.major = row['major']
	t.major_code = row['major_code']
	t.term = row['term']
	t.days = row['days']

	if row['start_time'].nil? || row['start_time'].empty? || row['start_time'] == "To be arranged"
		t.start_time = nil
	elsif row['start_time'].include? ":"
		t.start_time = Time.strptime(row['start_time'] + " UTC", '%l:%M%P %Z')
	else
		t.start_time = Time.strptime(row['start_time'] + " UTC", '%l%P %Z')
	end

	if row['end_time'].nil? || row['end_time'].empty? || row['end_time'] == "To be arranged"
		t.end_time = nil
	elsif row['end_time'].include? ":"
		t.end_time = Time.strptime(row['end_time'] + " UTC", '%l:%M%P %Z')
	else
		t.end_time = Time.strptime(row['end_time'] + " UTC", '%l%P %Z')
	end

	t.location = row['location']
	t.instructor = row['instructor']
	t.url = row['url']

	t.save
	puts "#{t.title} #{t.section} saved"
end

csv_class_similarity_file = File.read(Rails.root.join('lib', 'seeds', 'class_similarity.csv'))
class_similarity_csv = CSV.parse(csv_class_similarity_file, :headers => true, :encoding => 'UTF-8')
class_similarity_csv.each do |row|
	t = ClassSimilarity.new
	t.course_id = row['course_id']
	t.similar_course_id = row['similar_course_id']
	t.similarity = row['score']
	t.save
end

csv_requisites_file = File.read(Rails.root.join('lib', 'seeds', 'requisites.csv'))
requsites_csv = CSV.parse(csv_requisites_file, :headers => true, :encoding => 'UTF-8')
requsites_csv.each do |row|
	t = Requisite.new
	t.course_id = row['course_id']
	t.operator = row['operator']
	t.requisite_course_id_1 = row['requisite_course_id_1']
	t.requisite_course_id_2 = row['requisite_course_id_2']
	t.save
end

csv_ge_file = File.read(Rails.root.join('lib', 'seeds', 'ge_categories.csv'))
ge_csv = CSV.parse(csv_ge_file, :headers => true, :encoding => 'UTF-8')
ge_csv.each do |row|
	t = GeCategory.new
	t.course_id = row['course_id']
	t.foundation = row['foundation']
	t.category = row['category']
	t.save
end

csv_bruinwalk_file = File.read(Rails.root.join('lib', 'seeds', 'registrar_vs_bruinwalk_similiarity.csv'))
bruinwalk_csv = CSV.parse(csv_bruinwalk_file, :headers => true, :encoding => 'UTF-8')
bruinwalk_csv.each do |row|
	t = BruinwalkRating.new
	t.lecture_id = row['lecture_id']
	t.overall_rating = row['overall']
	t.easiness_rating = row['easiness']
	t.workload_rating = row['workload']
	t.clarity_rating = row['clarity']
	t.helpfulness_rating = row['helpfulness']
	t.save
end

ClassData.import

puts "There are now #{IndependentClassData.count} rows in the independent class data table"
puts "There are now #{DependentClassData.count} rows in the dependent class data table"
puts "There are now #{ClassData.count} rows in the class data table"
puts "There are now #{ClassSimilarity.count} rows in the class similarity table"
puts "There are now #{Requisite.count} rows in the requisites table"
puts "There are now #{GeCategory.count} rows in the ge categories table"
puts "There are now #{BruinwalkRating.count} rows in the bruinwalk ratings table"