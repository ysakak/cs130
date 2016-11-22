class ClassDataController < ApplicationController
  def index
    if (params[:major]) 
      @class_data = ClassData.where(major: params[:major])
    else 
      @class_data = ClassData.all
    end

    @col_count = 6
    render :layout => false
  end

  def show
    if (params[:id])
      @class_data = ClassData.find(params[:id])
      @independent_classes = @class_data.independent_classes
      total_similarities = @class_data.similar_classes
      @similar_classes = []

      for similarity in total_similarities.order('similarity desc')
        if similarity.similarity > 0.05
          @similar_classes.push(similarity.similar_class_data)
        end
      end

      @has_similar_classes = !@similar_classes.empty?
    end

    render :layout => false
  end
end
