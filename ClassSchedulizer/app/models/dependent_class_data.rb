class DependentClassData < ApplicationRecord
  belongs_to :independent_class, :class_name => 'IndependentClassData', :foreign_key => 'lecture_id'

  def days_to_array()
    day_mapper = {}
    day_mapper['Monday'] = 1
    day_mapper['Tuesday'] = 2
    day_mapper['Wednesday'] = 3
    day_mapper['Thursday'] = 4
    day_mapper['Friday'] = 5

    num_arr = Array.new

    string_arr = self.days.split(",")

    for day in string_arr 
      num_arr.push(day_mapper[day.delete(' ')])
    end

    return num_arr
  end

  def format_time(time)
    return time.strftime("%H:%M")
  end

  def as_json(options = {})
    if !self.start_time.nil?
      {
        :title => self.title,
        :start => format_time(self.start_time),
        :end => format_time(self.end_time),
        :dow => self.days_to_array(),
        :color => "green"
      }
    end
  end
end
