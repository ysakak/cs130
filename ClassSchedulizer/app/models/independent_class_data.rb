class IndependentClassData < ApplicationRecord
  has_many :dependent_classes, :class_name => 'DependentClassData', :primary_key => 'lecture_id', :foreign_key => 'lecture_id'
  belongs_to :class_data, :class_name => 'ClassData', :foreign_key => 'title'

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
    color_list = ["green", "olive", "yellow", "blue", "orange", "purple", "teal"]

    if !self.start_time.nil?
      {
        :id => self.lecture_id,
        :title => self.title,
        :start => format_time(self.start_time),
        :end => format_time(self.end_time),
        :dow => self.days_to_array(),
        :color => color_list[self.lecture_id % 7]
      }
    end
  end
end
