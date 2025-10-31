import praw
from datetime import datetime
from dotenv import load_dotenv
import os
import json

load_dotenv("C://Users//ryanh//code//projects//canucksTix//.env")

clientID = os.getenv("REDDIT_CLIENT_ID")
clientSecret = os.getenv("REDDIT_CLIENT_SECRET")
pw = os.getenv("REDDIT_PASSWORD")
userAgent = os.getenv("REDDIT_USER_AGENT")
username = os.getenv("REDDIT_USERNAME")

postID = "1nvaldi"


def getRedditInstance():
    reddit = praw.Reddit(
        client_id=clientID,
        client_secret=clientSecret,
        password=pw,
        user_agent=userAgent,
        username=username,
    )
    return reddit


def getComments():
    try:
        reddit = getRedditInstance()
        post = reddit.submission(id=postID)

        post.comments.replace_more(limit=None)
        flattened = post.comments.list()
        flattened.sort(key=lambda c: c.created_utc, reverse=True)

        res = []
        for i, c in enumerate(flattened):
            res.append(
                {
                    "index": i,
                    "author": str(c.author),
                    "body": c.body,
                    "created": datetime.fromtimestamp(c.created_utc).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "permalink": f"https://reddit.com{c.permalink}",
                }
            )

        return {
            "success": True,
            "comments": res,
        }
        # topLevelComments = [c for c in post.comments]

        # # sort comments by recent
        # topLevelComments.sort(key=lambda c: c.created_utc, reverse=True)

        # formattedComments = []
        # for c in topLevelComments:
        #     formattedComments.append(formatCommentTree(c, depth=0))

        # return {
        #     "success": True,
        #     "comments": formattedComments,
        # }
    except Exception as e:
        print(f"Error fetching Reddit data: {e}")
        return {
            "success": False,
            "error": str(e),
            "postTitle": "error loading thread",
            "postURL": "#",
            "comments": [],
        }


def getBodies(comments):
    res = []
    for c in comments["comments"]:
        res.append(c["body"])

    return res


# Testing
if __name__ == "__main__":
    print("Testing Reddit API...")
    data = getComments()

    if data["success"]:
        # print("\nFirst 3 comments:")
        # for comment in data["comments"][:3]:
        #     print(f"  - {comment['author']}: {comment['body'][:50]}...")
        # for comment in data["comments"]:
        #     print(comment)
        #     # bodies = getCommentBodies(comment)
        #     # print(bodies)
        #     print("================================")
        print(json.dumps(data, indent=2))

        bodies = getBodies(data)
        print(bodies)

    else:
        print(f"Error: {data.get('error', 'Unknown error')}")
