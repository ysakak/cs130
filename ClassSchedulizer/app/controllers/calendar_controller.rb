class CalendarController < ApplicationController
  def index
    # for demo only, remove later.
    @class = IndependentClassData.where(["title = 'Introduction to Computer Science I'"])[0]
    @dependent_class = DependentClassData.where(["class_id = 187093202"])[0]
    session[:chosen_classes] = []
    (session[:chosen_classes] ||= []) << @class
    (session[:chosen_classes] ||= []) << @dependent_class

    chosen_class_json_array = []

    for chosen_class in session[:chosen_classes]
      chosen_class_json_array.push(chosen_class.as_json)
    end

    @chosen_classes = chosen_class_json_array.to_json().html_safe()

  end
end
