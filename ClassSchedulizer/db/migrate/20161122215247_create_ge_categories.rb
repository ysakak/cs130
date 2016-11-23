class CreateGeCategories < ActiveRecord::Migration[5.0]
  def change
    create_table :ge_categories do |t|
      t.string :course_id
      t.string :foundation
      t.string :category
      t.timestamps
    end
  end
end
