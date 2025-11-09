import json
import sys
from pathlib import Path
from typing import List, Dict, Any


sys.path.insert(1, "C://Users//ryanh//code//projects//canucksTix//libs//reddit-api")
sys.path.insert(1, "C://Users//ryanh//code//projects//canucksTix//libs//gemini-api")
sys.path.insert(1, "C://Users//ryanh//code//projects//canucksTix")
import reddit_api
import gemini_api
from backend.db.database import SessionLocal
from backend.services.db_service import upsert_ticket_batch

# cache for testing
TESTING_DATA_DIR = Path(__file__).parent / "testingData"

REDDIT_CACHE = TESTING_DATA_DIR / "redditComments.json"
GEMINI_CACHE = TESTING_DATA_DIR / "geminiAnalysis.json"
MERGED_CACHE = TESTING_DATA_DIR / "merged.json"

USE_CACHE = False


def getAllListings():
    if USE_CACHE and REDDIT_CACHE.exists() and REDDIT_CACHE.stat().st_size > 0:
        print("📦 Using cached Reddit data")
        with open(REDDIT_CACHE, "r", encoding="utf-8") as f:
            comments = json.load(f)
    else:
        print("🌐 Fetching fresh Reddit data")
        comments = reddit_api.getComments()
        with open(REDDIT_CACHE, "w", encoding="utf-8") as f:
            json.dump(comments, f, indent=2)

    bodies = _getBodies(comments)

    if USE_CACHE and GEMINI_CACHE.exists and GEMINI_CACHE.stat().st_size > 0:
        print("📦 Using cached Gemini analysis")
        with open(GEMINI_CACHE, "r", encoding="utf-8") as f:
            analysis = json.load(f)
    else:
        print("🌐 Fetching fresh Gemini analysis")
        analysis = gemini_api.rateListings(bodies)
        with open(GEMINI_CACHE, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2)

    if USE_CACHE and MERGED_CACHE.exists and MERGED_CACHE.stat().st_size > 0:
        print("📦 Using cached merged data")
        with open(MERGED_CACHE, "r", encoding="utf-8") as f:
            mergedData = json.load(f)
    else:
        print("🌐 Fresh merge data")
        mergedData = _mergeAnalysis(comments, analysis)
        with open(MERGED_CACHE, "w", encoding="utf-8") as f:
            json.dump(mergedData, f, indent=2)

    try:
        db = SessionLocal()
        tickets_to_create = []
        for c_id, c_data in mergedData.items():
            ticket_data = {
                "source": "reddit",
                "author": c_data.get("author"),
                "body": c_data.get("body"),
                "created": c_data.get("created"),
                "permalink": c_data.get("permalink"),
                "location": c_data.get("location"),
                "price_per_ticket": c_data.get("price_per_ticket"),
                "quantity": c_data.get("quantity"),
                "game": c_data.get("game"),
                "rating": c_data.get("rating"),
                "description": c_data.get("description"),
            }
            tickets_to_create.append(ticket_data)

        upsert_ticket_batch(db, tickets_to_create)
    finally:
        db.close()

    return mergedData


def _getBodies(comments):
    res = []
    for c in comments["comments"].values():
        res.append(c["body"])

    return res


def _mergeAnalysis(comments, analysis):
    merged = {}
    for k, v in analysis.items():
        merged[k] = comments["comments"][k] | v

    keysToDelete = []
    for k, v in comments["comments"].items():
        if k not in merged.keys():
            keysToDelete.append(k)

    for k in keysToDelete:
        del comments["comments"][k]
    return merged


if __name__ == "__main__":
    data = getAllListings()
    print(json.dumps(data, indent=2))
    # comments, analysis = getAllListings()
    # print(json.dumps(comments, indent=2))
    # print(json.dumps(analysis, indent=2))
