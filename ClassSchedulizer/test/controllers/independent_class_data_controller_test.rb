require 'test_helper'

class IndependentClassDataControllerTest < ActionDispatch::IntegrationTest
  setup do
    @independent_class_data = independent_class_data(:one)
  end

  test "should get index" do
    get independent_class_data_url
    assert_response :success
  end

  test "should get new" do
    get new_independent_class_data_url
    assert_response :success
  end

  test "should create independent_class_data" do
    assert_difference('IndependentClassData.count') do
      post independent_class_data_url, params: { independent_class_data: { class_type: @independent_class_data.class_type, course_id: @independent_class_data.course_id, days: @independent_class_data.days, description: @independent_class_data.description, end_time: @independent_class_data.end_time, final_examination_date: @independent_class_data.final_examination_date, final_examination_day: @independent_class_data.final_examination_day, final_examination_time: @independent_class_data.final_examination_time, grade_type: @independent_class_data.grade_type, impacted_class: @independent_class_data.impacted_class, instructor: @independent_class_data.instructor, lecture_id: @independent_class_data.lecture_id, level: @independent_class_data.level, location: @independent_class_data.location, major: @independent_class_data.major, major_code: @independent_class_data.major_code, restrictions: @independent_class_data.restrictions, section: @independent_class_data.section, start_time: @independent_class_data.start_time, term: @independent_class_data.term, text_book_url: @independent_class_data.text_book_url, title: @independent_class_data.title, units: @independent_class_data.units, url: @independent_class_data.url } }
    end

    assert_redirected_to independent_class_data_url(IndependentClassData.last)
  end

  test "should show independent_class_data" do
    get independent_class_data_url(@independent_class_data)
    assert_response :success
  end

  test "should get edit" do
    get edit_independent_class_data_url(@independent_class_data)
    assert_response :success
  end

  test "should update independent_class_data" do
    patch independent_class_data_url(@independent_class_data), params: { independent_class_data: { class_type: @independent_class_data.class_type, course_id: @independent_class_data.course_id, days: @independent_class_data.days, description: @independent_class_data.description, end_time: @independent_class_data.end_time, final_examination_date: @independent_class_data.final_examination_date, final_examination_day: @independent_class_data.final_examination_day, final_examination_time: @independent_class_data.final_examination_time, grade_type: @independent_class_data.grade_type, impacted_class: @independent_class_data.impacted_class, instructor: @independent_class_data.instructor, lecture_id: @independent_class_data.lecture_id, level: @independent_class_data.level, location: @independent_class_data.location, major: @independent_class_data.major, major_code: @independent_class_data.major_code, restrictions: @independent_class_data.restrictions, section: @independent_class_data.section, start_time: @independent_class_data.start_time, term: @independent_class_data.term, text_book_url: @independent_class_data.text_book_url, title: @independent_class_data.title, units: @independent_class_data.units, url: @independent_class_data.url } }
    assert_redirected_to independent_class_data_url(@independent_class_data)
  end

  test "should destroy independent_class_data" do
    assert_difference('IndependentClassData.count', -1) do
      delete independent_class_data_url(@independent_class_data)
    end

    assert_redirected_to independent_class_data_url
  end
end
