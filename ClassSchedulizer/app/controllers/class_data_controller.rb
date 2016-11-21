class ClassDataController < ApplicationController
  def index
    class_data_params = params.slice(:major)
    if (class_data_params) 
      @class_data = ClassData.where(major: class_data_params['major'])
    else 
      @class_data = ClassData.all
    

    end

    @col_count = 6

  end

  def show
    @class_data = ClassData.find(params[:id])
    @independent_classes = @class_data.independent_classes
  end
end
