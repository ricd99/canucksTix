import json
import sys
from pathlib import Path
from typing import List, Dict, Any
import os

sys.path.insert(1, "C://Users//ryanh//code//projects//canucksTix//libs//reddit-api")
sys.path.insert(1, "C://Users//ryanh//code//projects//canucksTix//libs//gemini-api")
sys.path.insert(1, "C://Users//ryanh//code//projects//canucksTix")
import gemini_api
import reddit_api
from backend.db.database import SessionLocal
from backend.db.db_service import upsert_ticket_batch

sys.path.insert(1, "C://Users//ryanh//code//projects//canucksTix")
from backend.core.config import settings

db_path = settings.DATABASE_URL.replace("sqlite:///", "")
full_path = os.path.abspath(db_path)
print(f"📂 Database file location: {full_path}")
print(f"📄 File exists: {os.path.exists(full_path)}")
if os.path.exists(full_path):
    print(f"📊 File size: {os.path.getsize(full_path)} bytes")

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
        res = upsert_ticket_batch(db, mergedData)
        from backend.models.ticket import Ticket

        count = db.query(Ticket).count()
        print(f"Total tickets in database: {count}")
    except Exception as e:
        print(f"❌ Error upserting tickets: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()

    return res


def _getBodies(comments: Dict[str, Any]) -> List[str]:
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
    print(data)
    # print(json.dumps(data, indent=2))
