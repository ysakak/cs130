Rails.application.routes.draw do
  resources :requisites
  resources :class_data
  get 'calendar/index'

  resources :dependent_class_data
  resources :independent_class_data

  get 'class/details'

  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html

  root 'application#title'

  get '/calendar' => 'calendar#index'
  get '/search' => 'class_data#index'
  get '/class_data_search' => 'class_data#show'
  get '/independent_class_data_search' => 'independent_class_data#show'
  get '/add_section' => 'calendar#index'
  get '/calendar/view' => 'calendar#view'
end
