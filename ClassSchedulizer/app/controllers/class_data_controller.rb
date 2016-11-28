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

    if (params[:start_times])
      start_times = params[:start_times].split(",")
      end_times = params[:end_times].split(",")
      days_list = params[:days].split("|")

      for class_data in @class_data
        all_independent_classes_invalid = true

        for independent_class in class_data.independent_classes
          if !independent_class.overlap_times(start_times, end_times, days_list)
            all_independent_classes_invalid = false
          end
        end

        class_data.invalid = all_independent_classes_invalid
      end
    end

    if (params[:currClasses])
      curr_classes = params[:currClasses].split(",")

      for class_data in @class_data
        
        reqClasses = class_data.requisites
        reqStack = Array.new
        if reqClasses.length > 0
          reqClasses.each_with_index do |requisite, index|
            print reqClasses.length
            reqStack.push(requisite.requisite_course_id_1)
            unless requisite.requisite_course_id_2.nil? || requisite.requisite_course_id_2.empty?
              reqStack.push(requisite.operator)
              reqStack.push(requisite.requisite_course_id_2)
            end
            if index != reqClasses.size - 1
              reqStack.push("AND")
            end
          end
        end

        intersection = reqStack & curr_classes

        if !intersection.empty?
            class_data.invalid = true
        else
          class_data.invalid = false
        end

      end
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
      @reqstack = Array.new
      if @requisites.length > 0
        @requisites.each_with_index do |requisite, index|
          print @requisites.length
          @reqstack.push(requisite.requisite_course_id_1)
          unless requisite.requisite_course_id_2.nil? || requisite.requisite_course_id_2.empty?
            @reqstack.push(requisite.operator)
            @reqstack.push(requisite.requisite_course_id_2)
          end
          if index != @requisites.size - 1
            @reqstack.push("AND")
          end
        end
      end

      if (params[:currClasses])
        curr_classes = params[:currClasses].split(",")
        intersection = @reqstack & curr_classes

        for independent_class in @independent_classes
          if !intersection.empty?
            independent_class.invalid = true
          else
            independent_class.invalid = false
          end
        end
      end

      for similarity in total_similarities.order('similarity desc')
        if similarity.similarity > 0.05
          @similar_classes.push(similarity.similar_class_data)
        end
      end

      @has_similar_classes = !@similar_classes.empty?

      if (params[:start_times])
        start_times = params[:start_times].split(",")
        end_times = params[:end_times].split(",")
        days_list = params[:days].split("|")

        for independent_class in @independent_classes
          independent_class.invalid = independent_class.overlap_times(start_times, end_times, days_list)
        end
      end
    end

    render :layout => false
  end
end
