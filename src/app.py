import sys
from flask import Flask, request, render_template
import requests

sys.path.insert(
    1, "C://Users//ryanh//code//projects//canucksTix//libs//marketplace-api"
)

import MarketplaceAPI

app = Flask(__name__)

# testing url
baseURL = "http://127.0.0.1:5000/api/"


@app.route("/", methods=["GET"])
def home():
    return render_template("base.html")


@app.route("/api/locations", methods=["GET"])
def locations():
    locationQuery = request.args.get("locationQuery")

    result = MarketplaceAPI.handleLocations(locationQuery)
    return result


@app.route("/api/search", methods=["GET"])
def search():
    lat = request.args.get("locationLatitude")
    lon = request.args.get("locationLongitude")
    q = request.args.get("listingQuery")

    result = MarketplaceAPI.handleSearch(lat, lon, q)
    return result


if __name__ == "__main__":
    app.run(debug=True)
