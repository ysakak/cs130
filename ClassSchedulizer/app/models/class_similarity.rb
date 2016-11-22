class ClassSimilarity < ApplicationRecord
  belongs_to :class_data, :class_name => 'ClassData', :primary_key => 'course_id', :foreign_key => 'course_id'
  has_one :similar_class_data, :class_name => 'ClassData', :primary_key => 'similar_course_id', :foreign_key => 'course_id'
end