class GeCategory < ApplicationRecord
  belongs_to :class_data, :class_name => "ClassData", :primary_key => 'course_id', :foreign_key => 'course_id'
end
