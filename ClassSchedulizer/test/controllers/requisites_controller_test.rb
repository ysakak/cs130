require 'test_helper'

class RequisitesControllerTest < ActionDispatch::IntegrationTest
  setup do
    @requisite = requisites(:one)
  end

  test "should get index" do
    get requisites_url
    assert_response :success
  end

  test "should get new" do
    get new_requisite_url
    assert_response :success
  end

  test "should create requisite" do
    assert_difference('Requisite.count') do
      post requisites_url, params: { requisite: { course_id: @requisite.course_id, operator: @requisite.operator, requisite_course_id_1: @requisite.requisite_course_id_1, requisite_course_id_2: @requisite.requisite_course_id_2 } }
    end

    assert_redirected_to requisite_url(Requisite.last)
  end

  test "should show requisite" do
    get requisite_url(@requisite)
    assert_response :success
  end

  test "should get edit" do
    get edit_requisite_url(@requisite)
    assert_response :success
  end

  test "should update requisite" do
    patch requisite_url(@requisite), params: { requisite: { course_id: @requisite.course_id, operator: @requisite.operator, requisite_course_id_1: @requisite.requisite_course_id_1, requisite_course_id_2: @requisite.requisite_course_id_2 } }
    assert_redirected_to requisite_url(@requisite)
  end

  test "should destroy requisite" do
    assert_difference('Requisite.count', -1) do
      delete requisite_url(@requisite)
    end

    assert_redirected_to requisites_url
  end
end
