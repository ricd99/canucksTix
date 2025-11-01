import json
import sys
from typing import List, Dict, Any

sys.path.insert(1, "C://Users//ryanh//code//projects//canucksTix//libs//reddit-api")
sys.path.insert(1, "C://Users//ryanh//code//projects//canucksTix//libs//gemini-api")

import redditAPI
import geminiAPI


def getAllListings():
    comments = redditAPI.getComments()
    bodies = _getBodies(comments)
    analysis = geminiAPI.rateListings(bodies)
    return (comments, analysis)


def _getBodies(comments):
    res = []
    for c in comments["comments"]:
        res.append(c["body"])

    return res


if __name__ == "__main__":
    comments, analysis = getAllListings()
    print(json.dumps(comments, indent=2))
    # print(analysis)
    print(json.dumps(analysis, indent=2))
