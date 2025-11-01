import json
import sys
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(1, "C://Users//ryanh//code//projects//canucksTix//libs//reddit-api")
sys.path.insert(1, "C://Users//ryanh//code//projects//canucksTix//libs//gemini-api")

import redditAPI
import geminiAPI

# cache for testing
TESTING_DATA_DIR = Path(__file__).parent / "testingData"

REDDIT_CACHE = TESTING_DATA_DIR / "redditComments.json"
GEMINI_CACHE = TESTING_DATA_DIR / "geminiAnalysis.json"

USE_CACHE = True


def getAllListings():
    if USE_CACHE and REDDIT_CACHE.exists() and REDDIT_CACHE.stat().st_size > 0:
        print("📦 Using cached Reddit data")
        with open(REDDIT_CACHE, "r", encoding="utf-8") as f:
            comments = json.load(f)
    else:
        print("🌐 Fetching fresh Reddit data")
        comments = redditAPI.getComments()
        with open(REDDIT_CACHE, "w", encoding="utf-8") as f:
            json.dump(comments, f, indent=2)

    bodies = _getBodies(comments)

    if USE_CACHE and GEMINI_CACHE.exists and GEMINI_CACHE.stat().st_size > 0:
        print("📦 Using cached Gemini analysis")
        with open(GEMINI_CACHE, "r", encoding="utf-8") as f:
            analysis = json.load(f)
    else:
        analysis = geminiAPI.rateListings(bodies)
        with open(GEMINI_CACHE, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2)

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
