class AddCourseIdToClassData < ActiveRecord::Migration[5.0]
  def change
    add_column :class_data, :course_id, :string
  end
end
