require 'test_helper'

class IndependentClassDataControllerTest < ActionDispatch::IntegrationTest
  setup do
    @independent_class_data = independent_class_data(:one)
  end

  test "should get index" do
    get independent_class_data_index_url
    assert_response :success
  end

  test "should show independent_class_data" do
    get independent_class_data_url(@independent_class_data)
    assert_response :success
  end

  test "should get edit" do
    get edit_independent_class_data_url(@independent_class_data)
    assert_response :success
  end
end
