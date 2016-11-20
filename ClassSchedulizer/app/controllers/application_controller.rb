class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception

  def title
      render html: "Class Schedulizer"
  end
end
