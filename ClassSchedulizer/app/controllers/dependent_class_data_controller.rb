class DependentClassDataController < ApplicationController
  before_action :set_dependent_class_data, only: [:show, :edit, :update, :destroy]

  # GET /dependent_class_data
  # GET /dependent_class_data.json
  def index
    @dependent_class_data = DependentClassData.all
  end

  # GET /dependent_class_data/1
  # GET /dependent_class_data/1.json
  def show
  end

  # GET /dependent_class_data/new
  def new
    @dependent_class_data = DependentClassData.new
  end

  # GET /dependent_class_data/1/edit
  def edit
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_dependent_class_data
      @dependent_class_data = DependentClassData.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def dependent_class_data_params
      params.require(:dependent_class_data).permit(:class_id, :lecture_id, :class_type, :section, :course_id, :title, :major, :major_code, :term, :days, :start_time, :end_time, :location, :instructor, :url)
    end
end
