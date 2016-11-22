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
    end

    render layout: false
  end

  # GET /independent_class_data/new
  def new
    @independent_class_data = IndependentClassData.new
  end

  def show_selected
    @independent_classes = []
    @dependent_classes = []

    if (params[:independent_ids])
      independent_id_array = params[:independent_ids].split(',')
      for independent_id in independent_id_array
        @independent_classes.push(IndependentClassData.find_by(:lecture_id => independent_id))
      end
    end

    if (params[:dependent_ids])
      dependent_id_array = params[:dependent_ids].split(',')
      for dependent_id in dependent_id_array
        @dependent_classes.push(DependentClassData.find_by(:class_id => dependent_id))
      end
    end

    render layout: false
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
