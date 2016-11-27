#ui_test_spec.rb

require "spec_helper"
require "capybara/rspec"

feature "homepage has a calendar" do
  scenario "calendar has an ID of calendar" do
    visit "/calendar"

    calendar_elem = find_by_id("calendar")
    caleendar_class = calendar_elem[:class]

    expect(caleendar_class).to eql("fc fc-unthemed fc-ltr")
  end
end

feature "homepage has a searchbar" do 
	scenario "searchbar has a placeholder" do
		visit "/calendar"

		searchbar_elem = find_by_id("search")
		searchbar_ph = searchbar_elem[:placeholder]

		expect(searchbar_ph).to eql("Search your major")
	end
end