require 'test_helper'

class IndependentClassDataControllerTest < ActionDispatch::IntegrationTest
  setup do
    @independent_class_datum = independent_class_data(:one)
  end

  test "should get index" do
    get independent_class_data_url
    assert_response :success
  end

  test "should get new" do
    get new_independent_class_datum_url
    assert_response :success
  end

  test "should create independent_class_datum" do
    assert_difference('IndependentClassDatum.count') do
      post independent_class_data_url, params: { independent_class_datum: { class_type: @independent_class_datum.class_type, course_id: @independent_class_datum.course_id, days: @independent_class_datum.days, description: @independent_class_datum.description, end_time: @independent_class_datum.end_time, final_examination_date: @independent_class_datum.final_examination_date, final_examination_day: @independent_class_datum.final_examination_day, final_examination_time: @independent_class_datum.final_examination_time, grade_type: @independent_class_datum.grade_type, impacted_class: @independent_class_datum.impacted_class, instructor: @independent_class_datum.instructor, lecture_id: @independent_class_datum.lecture_id, level: @independent_class_datum.level, location: @independent_class_datum.location, major: @independent_class_datum.major, major_code: @independent_class_datum.major_code, restrictions: @independent_class_datum.restrictions, section: @independent_class_datum.section, start_time: @independent_class_datum.start_time, term: @independent_class_datum.term, text_book_url: @independent_class_datum.text_book_url, title: @independent_class_datum.title, units: @independent_class_datum.units, url: @independent_class_datum.url } }
    end

    assert_redirected_to independent_class_datum_url(IndependentClassDatum.last)
  end

  test "should show independent_class_datum" do
    get independent_class_datum_url(@independent_class_datum)
    assert_response :success
  end

  test "should get edit" do
    get edit_independent_class_datum_url(@independent_class_datum)
    assert_response :success
  end

  test "should update independent_class_datum" do
    patch independent_class_datum_url(@independent_class_datum), params: { independent_class_datum: { class_type: @independent_class_datum.class_type, course_id: @independent_class_datum.course_id, days: @independent_class_datum.days, description: @independent_class_datum.description, end_time: @independent_class_datum.end_time, final_examination_date: @independent_class_datum.final_examination_date, final_examination_day: @independent_class_datum.final_examination_day, final_examination_time: @independent_class_datum.final_examination_time, grade_type: @independent_class_datum.grade_type, impacted_class: @independent_class_datum.impacted_class, instructor: @independent_class_datum.instructor, lecture_id: @independent_class_datum.lecture_id, level: @independent_class_datum.level, location: @independent_class_datum.location, major: @independent_class_datum.major, major_code: @independent_class_datum.major_code, restrictions: @independent_class_datum.restrictions, section: @independent_class_datum.section, start_time: @independent_class_datum.start_time, term: @independent_class_datum.term, text_book_url: @independent_class_datum.text_book_url, title: @independent_class_datum.title, units: @independent_class_datum.units, url: @independent_class_datum.url } }
    assert_redirected_to independent_class_datum_url(@independent_class_datum)
  end

  test "should destroy independent_class_datum" do
    assert_difference('IndependentClassDatum.count', -1) do
      delete independent_class_datum_url(@independent_class_datum)
    end

    assert_redirected_to independent_class_data_url
  end
end
