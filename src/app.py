import sys
from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

sys.path.insert(
    1, "C://Users//ryanh//code//projects//canucksTix//libs//marketplace-api"
)

import MarketplaceAPI

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///locations.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class locations(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude


# testing url
baseURL = "http://127.0.0.1:5000/api/"


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/form", methods=["GET"])
def form():
    return render_template("form.html")


@app.route("/api/location", methods=["GET", "POST"])
def location():
    if request.method == "POST":
        locationQuery = request.form.get("loc")
    else:
        locationQuery = request.args.get("locationQuery")

    result = MarketplaceAPI.handleLocation(locationQuery)
    return result


@app.route("/api/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        lat = request.form.get("lat")
        lon = request.form.get("lon")
        q = request.form.get("q")
    else:
        lat = request.args.get("locationLatitude")
        lon = request.args.get("locationLongitude")
        q = request.args.get("listingQuery")

    result = MarketplaceAPI.handleSearch(lat, lon, q)
    return result


@app.route("/dummy", methods=["GET", "POST"])
def dummy():
    return "this is a dummy page"


if __name__ == "__main__":
    db.create_all
    app.run(debug=True)
