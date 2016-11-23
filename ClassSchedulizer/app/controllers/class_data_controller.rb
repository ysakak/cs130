class ClassDataController < ApplicationController
  def index
    if (params[:major]) 
      @class_data = ClassData.where(major: params[:major])
    elsif (params[:foundation])
      if (params[:category])
        @class_data = ClassData.joins(:ge_categories).where(:ge_categories => {foundation: params[:foundation], category: params[:category]})
      else
        @class_data = ClassData.joins(:ge_categories).where(:ge_categories => {foundation: params[:foundation]})
      end
    elsif (params[:keywords])
      results = ClassData.__elasticsearch__.search(
        query: {query_string: {
          query: params[:keywords]
        }},
        size: 1000
      )
      @class_data = results.records.to_a
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
      @requisites = @class_data.requisites

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
