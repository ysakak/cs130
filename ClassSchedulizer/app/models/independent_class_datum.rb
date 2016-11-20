class IndependentClassDatum < ApplicationRecord
	def self.search(search)
		if search
			self.where("major LIKE ?", "%#{search}%")
		else
			self.all
		end
	end
end
