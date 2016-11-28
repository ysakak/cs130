#ui_test_spec.rb

require "spec_helper"
require "capybara/rspec"

feature "homepage has a calendar" do
  scenario "calendar has an ID of calendar" do
    visit "/"

    calendar_elem = find_by_id("calendar")
    caleendar_class = calendar_elem[:class]

    expect(caleendar_class).to eql("fc fc-unthemed fc-ltr")
  end
end

feature "homepage has a searchbar" do 
	scenario "searchbar has a placeholder" do
		visit "/"

		searchbar_elem = find_by_id("search")
		searchbar_ph = searchbar_elem[:placeholder]

		expect(searchbar_ph).to eql("Search your major")
	end
end

feature "search and click result and back" do
	scenario "search computer science and click CS31" do
		visit "/"

		searchbar_elem = find_by_id('search')
		searchbar_elem.set("Computer Science")
		searchbar_elem.native.send_keys(:return)

		find('div', class: 'card-block',  text: 'COM SCI 31').click

		#find_by_id("class-details")
		find('div', id: 'class-data-header',text: "COM SCI 31 - Introduction to Computer Science I")

		find('a', text: "Lectures").click
		find('div', class: "active", id: "lectures", text: "Lectures")

		find_by_id("independent-class-btn").click
		find_by_id("independent-class-header")

		find('a', text: "Discussions").click
		find('div', class: "active", id: "dependent_classes", text: "Discussion Sections")		

		find_by_id("back-btn").click
		find_by_id("back-btn").click
		find('div', class: "card-deck-wrapper")
	end
end

feature "search and add class to schedule" do
	scenario "search mathematics and add 31A to schedule" do
		visit "/"

		searchbar_elem = find_by_id('search')
		searchbar_elem.set("Mathematics")
		searchbar_elem.native.send_keys(:return)

		find('div', class: 'card-block',  text: 'MATH 31A').click
		find('a', text: "Lectures").click
		first(:id, "independent-class-btn").click
		find('a', text: "Discussions").click
		first(:id, "add-section-btn").click

		page.has_css?('div .fc-title')
		first('div', class: "fc-title", text: "Differential and Integral Calculus")

	end
end

feature "search by GE category" do
	scenario "click search by GE and pick cateogries" do
		visit "/"

		find('a', text: "Search by GE Category").click

		select "Foundations of Arts and Humanities", :from => "foundation-search"
		select "Literary and Cultural Analysis", :from => "category-search"
		find_by_id("ge-search-submit").click

		find('div', class: 'card-block',  text: 'ART HIS 23')
	end
end

feature "search by keyword" do
	scenario "search by keyword and look for result" do
		visit "/"

		find('a', text: "Search by Keyword").click

		searchbar_elem = find_by_id("keyword-search")
		searchbar_elem.set("programming")

		find_by_id("keyword-search-submit").click

		first('div', class: 'card-block',  text: 'Programming Languages')
	end
end

feature "search, add, then delete class from schedule" do
	scenario "search, add, then delete. Check calendar" do
		visit "/"

		searchbar_elem = find_by_id('search')
		searchbar_elem.set("Physics")
		searchbar_elem.native.send_keys(:return)

		find('div', class: 'card-block',  text: 'PHYSICS 1A').click
		find('a', text: "Lectures").click
		first(:id, "independent-class-btn").click
		find('a', text: "Discussions").click
		first(:id, "add-section-btn").click

		page.has_css?('div .fc-title')
		first('div', class: "fc-title", text: "Physics for Scientists and Engineers: Mechanics")		

		find_by_id("delete-class-btn").click

		!page.has_css?('div .fc-title')
	end
end

feature "search, add, then clear calendar" do
	scenario "search Management, add class, then clear and check calendar" do
		visit "/"

		searchbar_elem = find_by_id('search')
		searchbar_elem.set("Physics")
		searchbar_elem.native.send_keys(:return)

		find('div', class: 'card-block',  text: 'PHYSICS 1A').click
		find('a', text: "Lectures").click
		first(:id, "independent-class-btn").click
		find('a', text: "Discussions").click
		first(:id, "add-section-btn").click

		page.has_css?('div .fc-title')
		first('div', class: "fc-title", text: "Physics for Scientists and Engineers: Mechanics")		

		find('input', id: "clear-calendar").click

		!page.has_css?('div .fc-title')
	end
end

feature "check requisite conflict" do
	scenario "Add CS31, then check that CS131 is conflicted" do
		visit "/"

		searchbar_elem = find_by_id('search')
		searchbar_elem.set("Computer Science")
		searchbar_elem.native.send_keys(:return)

		find('div', class: 'card-block',  text: 'COM SCI 33').click
		find('a', text: "Lectures").click
		first(:id, "independent-class-btn").click
		find('a', text: "Discussions").click
		first(:id, "add-section-btn").click

		page.has_css?('div .fc-title')
		first('div', class: "fc-title", text: "Introduction to Computer Organization")

		searchbar_elem.set("Computer Science")
		searchbar_elem.native.send_keys(:return)

		find('div', class: 'invalid-card',  text: 'COM SCI 131')
	end
end
