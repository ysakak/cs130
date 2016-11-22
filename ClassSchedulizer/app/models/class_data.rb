class ClassData < ApplicationRecord
    has_many :independent_classes, :class_name => 'IndependentClassData', :primary_key => 'title', :foreign_key => 'title'
    has_many :similar_classes, :class_name => 'ClassSimilarity', :primary_key => 'course_id', :foreign_key => 'course_id'
    has_many :requisites, :class_name => 'Requisite', :primary_key => 'course_id', :foreign_key => 'course_id'
    belongs_to :similar_to_classes, :class_name => 'ClassSimilarity', :primary_key => 'similar_course_id', :foreign_key => 'course_id'
    def self.search(search)
		if search
			self.where("major LIKE ?", "%#{search}%")
		else
			self.all
		end
	end
end
