require 'test_helper'

class DependentClassDataControllerTest < ActionDispatch::IntegrationTest
  setup do
    @dependent_class_data = dependent_class_data(:one)
  end

  test "should get index" do
    get dependent_class_data_index_url
    assert_response :success
  end

  test "should show dependent_class_data" do
    get dependent_class_data_url(@dependent_class_data)
    assert_response :success
  end

  test "should get edit" do
    get edit_dependent_class_data_url(@dependent_class_data)
    assert_response :success
  end
end
