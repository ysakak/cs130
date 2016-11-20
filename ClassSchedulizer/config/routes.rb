Rails.application.routes.draw do
  resources :dependent_class_data
  resources :independent_class_data

  get 'class/details'

  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html

  root 'application#title'
end
