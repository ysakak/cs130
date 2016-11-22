class RequisitesController < ApplicationController
  before_action :set_requisite, only: [:show, :edit, :update, :destroy]

  # GET /requisites
  # GET /requisites.json
  def index
    @requisites = Requisite.all
  end

  # GET /requisites/1
  # GET /requisites/1.json
  def show
  end

  # GET /requisites/new
  def new
    @requisite = Requisite.new
  end

  # GET /requisites/1/edit
  def edit
  end

  # POST /requisites
  # POST /requisites.json
  def create
    @requisite = Requisite.new(requisite_params)

    respond_to do |format|
      if @requisite.save
        format.html { redirect_to @requisite, notice: 'Requisite was successfully created.' }
        format.json { render :show, status: :created, location: @requisite }
      else
        format.html { render :new }
        format.json { render json: @requisite.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /requisites/1
  # PATCH/PUT /requisites/1.json
  def update
    respond_to do |format|
      if @requisite.update(requisite_params)
        format.html { redirect_to @requisite, notice: 'Requisite was successfully updated.' }
        format.json { render :show, status: :ok, location: @requisite }
      else
        format.html { render :edit }
        format.json { render json: @requisite.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /requisites/1
  # DELETE /requisites/1.json
  def destroy
    @requisite.destroy
    respond_to do |format|
      format.html { redirect_to requisites_url, notice: 'Requisite was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_requisite
      @requisite = Requisite.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def requisite_params
      params.require(:requisite).permit(:course_id, :operator, :requisite_course_id_1, :requisite_course_id_2)
    end
end
