class ClassDataController < ApplicationController
  def index
    @class_data = ClassData.all
  end

  def show
    @class_data = ClassData.find(params[:id])
  end
end
