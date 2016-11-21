class ClassDataController < ApplicationController
  def index
    if (params[:major]) 
      @class_data = ClassData.where(major: params[:major])
    else 
      @class_data = ClassData.all
    

    end

    @col_count = 6

  end

  def show
    if (params[:id])
      @class_data = ClassData.find(params[:id])
      @independent_classes = @class_data.independent_classes
      if (params[:major])
        @major = params[:major]
      end
    end
  end
end
