class CreateBruinwalkRatings < ActiveRecord::Migration[5.0]
  def change
    create_table :bruinwalk_ratings do |t|

      t.timestamps
    end
  end
end
