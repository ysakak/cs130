class CreateIndependentClassData < ActiveRecord::Migration[5.0]
  def change
    create_table :independent_class_data do |t|
      t.integer :lecture_id
      t.string :class_type
      t.integer :section
      t.string :course_id
      t.string :title
      t.string :major
      t.string :major_code
      t.string :term
      t.text :description
      t.string :days
      t.time :start_time
      t.time :end_time
      t.string :location
      t.integer :units
      t.string :instructor
      t.date :final_examination_date
      t.string :final_examination_day
      t.string :final_examination_time
      t.string :grade_type
      t.string :restrictions
      t.string :impacted_class
      t.string :level
      t.string :text_book_url
      t.string :url

      t.timestamps
    end
  end
end
