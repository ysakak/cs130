class ClassData < ApplicationRecord
    has_many :independent_classes, :class_name => 'IndependentClassData', :primary_key => 'title', :foreign_key => 'title'
end
