require 'elasticsearch/model'

class ClassData < ApplicationRecord
  include Elasticsearch::Model
  include Elasticsearch::Model::Callbacks
  attr_accessor :invalid
  alias_method :invalid?, :invalid
  
  has_many :independent_classes, :class_name => 'IndependentClassData', :primary_key => 'title', :foreign_key => 'title'
  has_many :similar_classes, :class_name => 'ClassSimilarity', :primary_key => 'course_id', :foreign_key => 'course_id'
  has_many :requisites, :class_name => 'Requisite', :primary_key => 'course_id', :foreign_key => 'course_id'
  has_one :ge_categories, :class_name => 'GeCategory', :primary_key => 'course_id', :foreign_key => 'course_id'
  belongs_to :similar_to_classes, :class_name => 'ClassSimilarity', :primary_key => 'similar_course_id', :foreign_key => 'course_id'
  
end
