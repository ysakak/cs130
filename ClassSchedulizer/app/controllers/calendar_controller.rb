class CalendarController < ApplicationController
  def index
  end

  def clear
    @chosen_classes = []
    @ind_class_ids = ""
    @disc_ids = ""
    render :layout => false
  end

  def view
    chosen_classes = []
    if (params[:ind_class_ids])
      for ind_class_id in params[:ind_class_ids].split(',')
        new_class = IndependentClassData.find(ind_class_id)
        chosen_classes << new_class
      end
    end

    if (params[:disc_ids])
      for disc_id in params[:disc_ids].split(',')
        new_dependent_class = DependentClassData.find(disc_id)
        chosen_classes << new_dependent_class
      end
    end

    if (params[:ind_class_id])
      new_class = IndependentClassData.find(params[:ind_class_id])
      chosen_classes << new_class
    end

    if (params[:disc_id])
      new_class = DependentClassData.find(params[:disc_id])
      chosen_classes << new_class
    end

    @chosen_class_json_array = []

    if !chosen_classes.nil?
      for chosen_class in chosen_classes
        @chosen_class_json_array.push(chosen_class.as_json)
      end
    end

    @chosen_classes = @chosen_class_json_array.to_json().html_safe()
    @ind_class_ids = params[:ind_class_ids]
    @disc_ids = params[:disc_ids]
    render :layout => false
  end
end
