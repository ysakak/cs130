class ClassSimilarity < ApplicationRecord
  belongs_to :class_data, :class_name => 'ClassData', :primary_key => 'course_id', :foreign_key => 'course_id'
  has_many :similar_class_data, :class_name => 'ClassData', :primary_key => 'course_id', :foreign_key => 'similar_course_id'
end