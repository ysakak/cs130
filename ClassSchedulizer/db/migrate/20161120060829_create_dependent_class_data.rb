class CreateDependentClassData < ActiveRecord::Migration[5.0]
  def change
    create_table :dependent_class_data do |t|
      t.integer :class_id
      t.integer :lecture_id
      t.string :class_type
      t.string :section
      t.string :course_id
      t.string :title
      t.string :major
      t.string :major_code
      t.string :term
      t.string :days
      t.time :start_time
      t.time :end_time
      t.string :location
      t.string :instructor
      t.string :url

      t.timestamps
    end
  end
end
