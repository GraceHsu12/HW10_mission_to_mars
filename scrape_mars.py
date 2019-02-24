#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import pymongo

from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import time


def init_browser():
	executable_path = {'executable_path': 'C:/Users/ricem/chromedriver.exe'}
	browser = Browser('chrome', **executable_path, headless=False)


def scrape():

	# store scrapped data into the dictionary mars_dict
	mars_dict = {}

	#########################################################

	## NASA Mars News
	url="https://mars.nasa.gov/#news_and_events"
	response = requests.get(url)


	bs_response = bs(response.text, 'html.parser')

	# Find all article information
	list_texts =bs_response.find_all('div', class_="list_text")
	

	# Get first article information
	first_article = list_texts[0]
	

	# Retrieve news title of latest article
	news_title = first_article.find('h3', class_="title").text
	news_title = news_title.split('\n')
	mars_dict["latest_news_title"] = news_title[1]
	

	# Find first description for the first article
	paragraph = bs_response.find('div', class_="description").text
	
	news_p = paragraph.split('\n')
	mars_dict["latest_news_paragraph"] = news_p[1]
	
	#########################################################

	## JPL Mars Space Images - Featured Image
	browser = init_browser()

	# Navigate to the specified url
	url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(url)

	time.sleep(1)

	# Click the featured image
	browser.find_by_xpath('//*[@id="full_image"]').click()

	# right click the enlarged image to copy image address manually
	browser.find_by_css('div.fancybox-inner').right_click()

	mars_dict["featured_image_url"] = "https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA19977_ip.jpg"


	#########################################################

	## Mars Weather

	# Access the Mars twitter site
	mars_twitter_url = "https://twitter.com/marswxreport?lang=en"
	mars_twit_response=requests.get(mars_twitter_url)

	# Use beautiful soup 
	mars_twits_soup = bs(mars_twit_response.text, 'html.parser')

	# Create a list of all tweets on the webpage
	all_twits = mars_twits_soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

	for twit in all_twits:
	    current_twit = twit.text
	    split_twit = current_twit.split(' ')
	    if split_twit[0] == 'InSight' or split_twit[0]=='Sol':
	        mars_weather = current_twit
	        break

	mars_dict["mars_weather"] = mars_weather

	#########################################################

	## Mars Facts

	# read html from the url and convert it to a list
	mars_facts_url="https://space-facts.com/mars/"
	tables = pd.read_html(mars_facts_url)

	mars_facts_df = tables[0]

	# Rename column titles
	mars_facts_df.columns= ["Description", "Value"]

	# Set index to Mars Facts
	mars_facts_df.set_index("Description", inplace=True)

	# convert table to html
	mars_html=mars_facts_df.to_html()

	# Remove \n's
	mars_dict["mars_html"] = mars_html.replace("\n", "")

	#########################################################

	## Mars Hemispheres
	# Went to the site and manually grabbed urls for images
	# Save each of Mar's hemispheres title(name) and img_url into a list of dictionaries
	hemisphere_image_urls = [
	    {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
	    {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
	    {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
	    {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
	]

	mars_dict["hemispheres_images"]

	browser.quit()

	return mars_dict