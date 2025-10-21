import MarketplaceScraper


def handleLocation(locationQuery):
    response = {}

    if locationQuery:
        status, error, data = MarketplaceScraper.getLocations(
            locationQuery=locationQuery
        )
    else:
        status = "Failure"
        error = {}
        error["source"] = "User"
        error["message"] = "Missing required parameter"
        data = {}

    response["status"] = status
    response["error"] = error
    response["data"] = data

    return response


def handleSearch(locationLatitude, locationLongitude, listingQuery):
    response = {}

    if locationLatitude and locationLongitude and listingQuery:
        status, error, data = MarketplaceScraper.getListings(
            locationLatitude=locationLatitude,
            locationLongitude=locationLongitude,
            listingQuery=listingQuery,
        )
    else:
        status = "Failure"
        error = {}
        error["source"] = "User"
        error["message"] = "Missing required parameter(s)"
        data = {}

    response["status"] = status
    response["error"] = error
    response["data"] = data

    return response
