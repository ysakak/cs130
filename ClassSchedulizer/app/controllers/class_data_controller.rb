class ClassDataController < ApplicationController
  def index
    @class_data = ClassData.all
  end

  def show
    @class_data = ClassData.find(params[:id])
    @independent_classes = IndependentClassData.where(title: @class_data.title)
  end
end
