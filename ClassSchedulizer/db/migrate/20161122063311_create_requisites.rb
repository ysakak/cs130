class CreateRequisites < ActiveRecord::Migration[5.0]
  def change
    create_table :requisites do |t|
      t.string :course_id
      t.string :operator
      t.string :requisite_course_id_1
      t.string :requisite_course_id_2

      t.timestamps
    end
  end
end
