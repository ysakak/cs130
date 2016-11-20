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
csv.each do |row|
	t = IndependentClassDatum.new
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
end

csv_dependent_class = File.read(Rails.root.join('lib', 'seeds', 'dependent_class_data.csv'))
csv = CSV.parse(csv_dependent_class, :headers => true, :encoding => 'UTF-8')
csv.each do |row|
	t = DependentClassDatum.new
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

puts "There are now #{IndependentClassDatum.count} rows in the independent class data table"
puts "There are now #{DependentClassDatum.count} rows in the dependent class data table"