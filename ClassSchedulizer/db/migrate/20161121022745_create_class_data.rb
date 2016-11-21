class CreateClassData < ActiveRecord::Migration[5.0]
  def change
    create_table :class_data do |t|
      t.string :title
      t.string :major
      t.string :major_code
      t.string :term
      t.text :description
      t.integer :units
      t.string :grade_type
      t.string :restrictions
      t.string :impacted_class
      t.string :level
    end
  end
end
