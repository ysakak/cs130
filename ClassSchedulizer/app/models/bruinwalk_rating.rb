class BruinwalkRating < ApplicationRecord
  belongs_to :independent_class_data, :class_name => "IndependentClassData", :primary_key => 'lecture_id', :foreign_key => 'lecture_id'
end
