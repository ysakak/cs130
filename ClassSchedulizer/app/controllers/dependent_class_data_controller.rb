class DependentClassDataController < ApplicationController
  before_action :set_dependent_class_datum, only: [:show, :edit, :update, :destroy]

  # GET /dependent_class_data
  # GET /dependent_class_data.json
  def index
    @dependent_class_data = DependentClassDatum.all
  end

  # GET /dependent_class_data/1
  # GET /dependent_class_data/1.json
  def show
  end

  # GET /dependent_class_data/new
  def new
    @dependent_class_datum = DependentClassDatum.new
  end

  # GET /dependent_class_data/1/edit
  def edit
  end

  # POST /dependent_class_data
  # POST /dependent_class_data.json
  def create
    @dependent_class_datum = DependentClassDatum.new(dependent_class_datum_params)

    respond_to do |format|
      if @dependent_class_datum.save
        format.html { redirect_to @dependent_class_datum, notice: 'Dependent class datum was successfully created.' }
        format.json { render :show, status: :created, location: @dependent_class_datum }
      else
        format.html { render :new }
        format.json { render json: @dependent_class_datum.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /dependent_class_data/1
  # PATCH/PUT /dependent_class_data/1.json
  def update
    respond_to do |format|
      if @dependent_class_datum.update(dependent_class_datum_params)
        format.html { redirect_to @dependent_class_datum, notice: 'Dependent class datum was successfully updated.' }
        format.json { render :show, status: :ok, location: @dependent_class_datum }
      else
        format.html { render :edit }
        format.json { render json: @dependent_class_datum.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /dependent_class_data/1
  # DELETE /dependent_class_data/1.json
  def destroy
    @dependent_class_datum.destroy
    respond_to do |format|
      format.html { redirect_to dependent_class_data_url, notice: 'Dependent class datum was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_dependent_class_datum
      @dependent_class_datum = DependentClassDatum.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def dependent_class_datum_params
      params.require(:dependent_class_datum).permit(:class_id, :lecture_id, :class_type, :section, :course_id, :title, :major, :major_code, :term, :days, :start_time, :end_time, :location, :instructor, :url)
    end
end
