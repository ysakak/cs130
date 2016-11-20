class CalendarController < ApplicationController
  def index
    # for demo only, remove later.
    @class = IndependentClassData.where(["title = 'Introduction to Computer Science I'"])[0]
    session[:chosen_classes] = []
    (session[:chosen_classes] ||= []) << @class.as_json()

    @chosen_classes = session[:chosen_classes].to_json.html_safe

  end
end
