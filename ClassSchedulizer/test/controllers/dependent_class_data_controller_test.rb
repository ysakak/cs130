require 'test_helper'

class DependentClassDataControllerTest < ActionDispatch::IntegrationTest
  setup do
    @dependent_class_data = dependent_class_data(:one)
  end

  test "should get index" do
    get dependent_class_data_url
    assert_response :success
  end

  test "should get new" do
    get new_dependent_class_data_url
    assert_response :success
  end

  test "should create dependent_class_data" do
    assert_difference('DependentClassData.count') do
      post dependent_class_data_url, params: { dependent_class_data: { class_id: @dependent_class_data.class_id, class_type: @dependent_class_data.class_type, course_id: @dependent_class_data.course_id, days: @dependent_class_data.days, end_time: @dependent_class_data.end_time, instructor: @dependent_class_data.instructor, lecture_id: @dependent_class_data.lecture_id, location: @dependent_class_data.location, major: @dependent_class_data.major, major_code: @dependent_class_data.major_code, section: @dependent_class_data.section, start_time: @dependent_class_data.start_time, term: @dependent_class_data.term, title: @dependent_class_data.title, url: @dependent_class_data.url } }
    end

    assert_redirected_to dependent_class_data_url(DependentClassData.last)
  end

  test "should show dependent_class_data" do
    get dependent_class_data_url(@dependent_class_data)
    assert_response :success
  end

  test "should get edit" do
    get edit_dependent_class_data_url(@dependent_class_data)
    assert_response :success
  end

  test "should update dependent_class_data" do
    patch dependent_class_data_url(@dependent_class_data), params: { dependent_class_data: { class_id: @dependent_class_data.class_id, class_type: @dependent_class_data.class_type, course_id: @dependent_class_data.course_id, days: @dependent_class_data.days, end_time: @dependent_class_data.end_time, instructor: @dependent_class_data.instructor, lecture_id: @dependent_class_data.lecture_id, location: @dependent_class_data.location, major: @dependent_class_data.major, major_code: @dependent_class_data.major_code, section: @dependent_class_data.section, start_time: @dependent_class_data.start_time, term: @dependent_class_data.term, title: @dependent_class_data.title, url: @dependent_class_data.url } }
    assert_redirected_to dependent_class_data_url(@dependent_class_data)
  end

  test "should destroy dependent_class_data" do
    assert_difference('DependentClassData.count', -1) do
      delete dependent_class_data_url(@dependent_class_data)
    end

    assert_redirected_to dependent_class_data_url
  end
end
