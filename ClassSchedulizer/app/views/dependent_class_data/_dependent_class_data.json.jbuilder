json.extract! dependent_class_data, :id, :class_id, :lecture_id, :class_type, :section, :course_id, :title, :major, :major_code, :term, :days, :start_time, :end_time, :location, :instructor, :url, :created_at, :updated_at
json.url dependent_class_data_url(dependent_class_data, format: :json)