require 'test_helper'

class DependentClassDataControllerTest < ActionDispatch::IntegrationTest
  setup do
    @dependent_class_datum = dependent_class_data(:one)
  end

  test "should get index" do
    get dependent_class_data_url
    assert_response :success
  end

  test "should get new" do
    get new_dependent_class_datum_url
    assert_response :success
  end

  test "should create dependent_class_datum" do
    assert_difference('DependentClassDatum.count') do
      post dependent_class_data_url, params: { dependent_class_datum: { class_id: @dependent_class_datum.class_id, class_type: @dependent_class_datum.class_type, course_id: @dependent_class_datum.course_id, days: @dependent_class_datum.days, end_time: @dependent_class_datum.end_time, instructor: @dependent_class_datum.instructor, lecture_id: @dependent_class_datum.lecture_id, location: @dependent_class_datum.location, major: @dependent_class_datum.major, major_code: @dependent_class_datum.major_code, section: @dependent_class_datum.section, start_time: @dependent_class_datum.start_time, term: @dependent_class_datum.term, title: @dependent_class_datum.title, url: @dependent_class_datum.url } }
    end

    assert_redirected_to dependent_class_datum_url(DependentClassDatum.last)
  end

  test "should show dependent_class_datum" do
    get dependent_class_datum_url(@dependent_class_datum)
    assert_response :success
  end

  test "should get edit" do
    get edit_dependent_class_datum_url(@dependent_class_datum)
    assert_response :success
  end

  test "should update dependent_class_datum" do
    patch dependent_class_datum_url(@dependent_class_datum), params: { dependent_class_datum: { class_id: @dependent_class_datum.class_id, class_type: @dependent_class_datum.class_type, course_id: @dependent_class_datum.course_id, days: @dependent_class_datum.days, end_time: @dependent_class_datum.end_time, instructor: @dependent_class_datum.instructor, lecture_id: @dependent_class_datum.lecture_id, location: @dependent_class_datum.location, major: @dependent_class_datum.major, major_code: @dependent_class_datum.major_code, section: @dependent_class_datum.section, start_time: @dependent_class_datum.start_time, term: @dependent_class_datum.term, title: @dependent_class_datum.title, url: @dependent_class_datum.url } }
    assert_redirected_to dependent_class_datum_url(@dependent_class_datum)
  end

  test "should destroy dependent_class_datum" do
    assert_difference('DependentClassDatum.count', -1) do
      delete dependent_class_datum_url(@dependent_class_datum)
    end

    assert_redirected_to dependent_class_data_url
  end
end
