import praw
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv("C://Users//ryanh//code//projects//canucksTix//.env")

clientID = os.getenv("REDDIT_CLIENT_ID")
clientSecret = os.getenv("REDDIT_CLIENT_SECRET")
pw = os.getenv("REDDIT_PASSWORD")
userAgent = os.getenv("REDDIT_USER_AGENT")
username = os.getenv("REDDIT_USERNAME")

postID = "1nvaldi"


def getComments():
    try:
        reddit = getRedditInstance()
        post = reddit.submission(id=postID)

        post.comments.replace_more(limit=None)
        allComments = post.comments.list()

        # sort comments by recent
        allComments.sort(key=lambda c: c.created_utc, reverse=True)

        formattedComments = []
        for c in allComments:
            formattedComments.append(
                {
                    "author": str(c.author),
                    "body": c.body,
                    "created": datetime.fromtimestamp(c.created_utc).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "createdUTC": c.created_utc,
                    "permalink": f"https://reddit.com{c.permalink}",
                }
            )

        return {
            "success": True,
            "postTitle": post.title,
            "postURL": post.url,
            "postAuthor": str(post.author),
            "commentCount": len(formattedComments),
            "comments": formattedComments,
        }
    except Exception as e:
        print(f"Error fetching Reddit data: {e}")
        return {
            "success": False,
            "error": str(e),
            "postTitle": "error loading thread",
            "postURL": "#",
            "comments": [],
        }


def getRedditInstance():
    reddit = praw.Reddit(
        client_id=clientID,
        client_secret=clientSecret,
        password=pw,
        user_agent=userAgent,
        username=username,
    )
    return reddit


# Testing
if __name__ == "__main__":
    print("Testing Reddit API...")
    data = getComments()

    if data["success"]:
        print(f"Post: {data['postTitle']}")
        print(f"Total comments: {data['commentCount']}")
        print("\nFirst 3 comments:")
        for comment in data["comments"][:3]:
            print(f"  - {comment['author']}: {comment['body'][:50]}...")
    else:
        print(f"Error: {data.get('error', 'Unknown error')}")
