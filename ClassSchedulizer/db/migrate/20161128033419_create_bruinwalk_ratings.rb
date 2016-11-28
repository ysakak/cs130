class CreateBruinwalkRatings < ActiveRecord::Migration[5.0]
  def change
    create_table :bruinwalk_ratings do |t|
      t.integer :lecture_id
      t.float :overall_rating
      t.float :easiness_rating
      t.float :workload_rating
      t.float :clarity_rating
      t.float :helpfulness_rating
      t.timestamps
    end
  end
end
