class CalendarController < ApplicationController
  def index
    # for demo only, remove later.
    @class = IndependentClassData.where(["title = 'Introduction to Computer Science I'"])[0]
    session[:chosen_classes] = []
    (session[:chosen_classes] ||= []) << @class

    chosen_class_json_array = []
    
    for chosen_class in session[:chosen_classes]
      chosen_class_json_array.push(chosen_class.as_json)
      for dependent_class in chosen_class.dependent_classes
        chosen_class_json_array.push(dependent_class.as_json)
      end
    end

    @chosen_classes = chosen_class_json_array.to_json().html_safe()

  end
end
