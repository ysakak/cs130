class ClassDataController < ApplicationController
  def index
    @class_data = ClassData.search(params[:search])

    respond_to do |format|
    	format.html
    	format.js
    end

  end

  def show
    @class_data = ClassData.find(params[:id])
    @independent_classes = @class_data.independent_classes
  end
end
