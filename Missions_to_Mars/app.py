from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection to db (mission_to_mars)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")

# Find the documents from the db collection (mars_info) and put them in a variable (mars_info)
@app.route("/")
def index():
# Find one record of data from the mongo database   
    mars_info = mongo.db.mars_info.find_one()

# Return the template and data   
    return render_template("index.html", mars_info=mars_info)

# Route that will trigger the scrape function to populate the db 
@app.route("/scrape")
def scrape():

# Run the scrape function
# Update the Mongo database using update and upsert=True  
    mars_info = mongo.db.mars_info
    mars_info_data = scrape_mars.scrape()
    mars_info.update({}, mars_info_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
