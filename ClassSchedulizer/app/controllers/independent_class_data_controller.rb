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
  end

  # GET /independent_class_data/new
  def new
    @independent_class_data = IndependentClassData.new
  end

  # GET /independent_class_data/1/edit
  def edit
  end

  # POST /independent_class_data
  # POST /independent_class_data.json
  def create
    @independent_class_data = IndependentClassData.new(independent_class_data_params)

    respond_to do |format|
      if @independent_class_data.save
        format.html { redirect_to @independent_class_data, notice: 'Independent class datum was successfully created.' }
        format.json { render :show, status: :created, location: @independent_class_data }
      else
        format.html { render :new }
        format.json { render json: @independent_class_data.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /independent_class_data/1
  # PATCH/PUT /independent_class_data/1.json
  def update
    respond_to do |format|
      if @independent_class_data.update(independent_class_data_params)
        format.html { redirect_to @independent_class_data, notice: 'Independent class datum was successfully updated.' }
        format.json { render :show, status: :ok, location: @independent_class_data }
      else
        format.html { render :edit }
        format.json { render json: @independent_class_data.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /independent_class_data/1
  # DELETE /independent_class_data/1.json
  def destroy
    @independent_class_data.destroy
    respond_to do |format|
      format.html { redirect_to independent_class_data_url, notice: 'Independent class datum was successfully destroyed.' }
      format.json { head :no_content }
    end
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
