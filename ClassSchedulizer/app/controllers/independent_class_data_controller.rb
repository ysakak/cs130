class IndependentClassDataController < ApplicationController
  before_action :set_independent_class_data, only: [:show, :edit, :update, :destroy]

  # GET /independent_class_data
  # GET /independent_class_data.json
  def index
    @independent_class_data = IndependentClassData.all
  end

  # GET /independent_class_data/1
  # GET /independent_class_data/1.json
  def show
    if (params[:id])
      @independent_class_data = IndependentClassData.find(params[:id])
      @dependent_classes = @independent_class_data.dependent_classes
      if (params[:class_id])
        @class_id = params[:class_id]
      end
      if (params[:major])
        @major = params[:major]
      end
    end
  end

  # GET /independent_class_data/new
  def new
    @independent_class_data = IndependentClassData.new
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_independent_class_data
      @independent_class_data = IndependentClassData.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def independent_class_data_params
      params.require(:independent_class_data).permit(:lecture_id, :class_type, :section, :course_id, :title, :major, :major_code, :term, :description, :days, :start_time, :end_time, :location, :units, :instructor, :final_examination_date, :final_examination_day, :final_examination_time, :grade_type, :restrictions, :impacted_class, :level, :text_book_url, :url)
    end
end
