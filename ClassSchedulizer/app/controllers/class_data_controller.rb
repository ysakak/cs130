class ClassDataController < ApplicationController
  def index
    @class_data = ClassData.search(params[:search])
  end

  def show
    @class_data = ClassData.find(params[:id])
    @independent_classes = IndependentClassData.where(title: @class_data.title)
  end
end
