class CreateClassSimilarities < ActiveRecord::Migration[5.0]
  def change
    create_table :class_similarities do |t|
      t.string :course_id
      t.string :similar_course_id
      t.float :similarity
      t.timestamps
    end
  end
end
