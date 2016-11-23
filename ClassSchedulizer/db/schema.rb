# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20161122215247) do

  create_table "class_data", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=utf8" do |t|
    t.string  "title"
    t.string  "major"
    t.string  "major_code"
    t.string  "term"
    t.text    "description",    limit: 65535
    t.integer "units"
    t.string  "grade_type"
    t.string  "restrictions"
    t.string  "impacted_class"
    t.string  "level"
    t.string  "course_id"
  end

  create_table "class_similarities", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=utf8" do |t|
    t.string   "course_id"
    t.string   "similar_course_id"
    t.float    "similarity",        limit: 24
    t.datetime "created_at",                   null: false
    t.datetime "updated_at",                   null: false
  end

  create_table "dependent_class_data", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=utf8" do |t|
    t.integer  "class_id"
    t.integer  "lecture_id"
    t.string   "class_type"
    t.string   "section"
    t.string   "course_id"
    t.string   "title"
    t.string   "major"
    t.string   "major_code"
    t.string   "term"
    t.string   "days"
    t.time     "start_time"
    t.time     "end_time"
    t.string   "location"
    t.string   "instructor"
    t.string   "url"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "ge_categories", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=utf8" do |t|
    t.string   "course_id"
    t.string   "foundation"
    t.string   "category"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "independent_class_data", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=utf8" do |t|
    t.integer  "lecture_id"
    t.string   "class_type"
    t.integer  "section"
    t.string   "course_id"
    t.string   "title"
    t.string   "major"
    t.string   "major_code"
    t.string   "term"
    t.text     "description",            limit: 65535
    t.string   "days"
    t.time     "start_time"
    t.time     "end_time"
    t.string   "location"
    t.integer  "units"
    t.string   "instructor"
    t.date     "final_examination_date"
    t.string   "final_examination_day"
    t.string   "final_examination_time"
    t.string   "grade_type"
    t.string   "restrictions"
    t.string   "impacted_class"
    t.string   "level"
    t.string   "text_book_url"
    t.string   "url"
    t.datetime "created_at",                           null: false
    t.datetime "updated_at",                           null: false
  end

  create_table "requisites", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=utf8" do |t|
    t.string   "course_id"
    t.string   "operator"
    t.string   "requisite_course_id_1"
    t.string   "requisite_course_id_2"
    t.datetime "created_at",            null: false
    t.datetime "updated_at",            null: false
  end

end
