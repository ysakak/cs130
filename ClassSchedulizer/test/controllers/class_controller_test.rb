require 'test_helper'

class ClassControllerTest < ActionDispatch::IntegrationTest
  test "should get details" do
    get class_details_url
    assert_response :success
  end

end
