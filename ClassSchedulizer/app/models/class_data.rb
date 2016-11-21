class ClassData < ApplicationRecord
    has_many :independent_classes, :class_name => 'IndependentClassData', :primary_key => 'title', :foreign_key => 'title'

    def self.search(search)
		if search
			self.where("major LIKE ?", "%#{search}%")
		else
			self.all
		end
	end
end
