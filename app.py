from flask import Flask, render_template, redirect
from scrape_mars import scrape
import pymongo
from flask_pymongo import PyMongo
from splinter import Browser

app=Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_facts")

@app.route("/")
def index():
	mars_scrape_results = mongo.db.collection.find
	return render_template("index.html", mars_scrape=mars_scrape_results)



@app.route("/scrape")
def scraper():

	mars_scrape_results = scrape()
	mongo.db.collection.update({}, mars_scrape_results, upsert=True)

	return redirect("/", code=302)



if __name__=='__main__':
	app.run(debug=True)