from google import genai
from dotenv import load_dotenv
import os
from pathlib import Path
import sys
import json

sys.path.insert(1, "C://Users//ryanh//code//projects//canucksTix//libs//reddit-api")
import reddit_api

from backend.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def rateListings(bodies):
    promptTemplate = getPromptTemplate()

    bodiesText = "\n\n".join(
        [f"COMMENT #{i}: \n{body}" for i, body in enumerate(bodies)]
    )

    prompt = promptTemplate + "\n\n" + bodiesText

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            # config={
            #     "system_instruction": """ You are an incredibly smart ticket agent who can make an accurate estimation of a ticket's value for a Canucks game
            #     considering its price and seat location in Rogers Arena""",
            #     "temperature": 0.7,
            # },
        )

        responseText = response.text.strip()

        start = responseText.find("{")
        end = responseText.rfind("}") + 1

        if (start != -1) and (end != -1):
            jsonString = responseText[start:end]
            analysis = json.loads(jsonString)
        else:
            print("No JSON found in response")
            analysis = {}

        return analysis
    except Exception as e:
        print(f"Error analyzing batch: {e}")


def getPromptTemplate():
    currentPath = Path(__file__)  # geminiAPI.py
    root = currentPath.parent.parent.parent  # canucksTix/
    promptPath = root / "backend" / "constants" / "geminiPrompt.txt"
    with open(promptPath, "r", encoding="utf-8") as f:
        return f.read()


# keep your eyes out for free deals (e.g. "first to guess my favourite player"), links to other pages to sell tickets,
# eliminate "ISO" (in search of)
# store data in database for training later on

# if __name__ == "__main__":
#     data = redditAPI.getComments()

#     print(rateListings(redditAPI.getBodies(data)))
