from google import genai
from dotenv import load_dotenv
import os
import inspect

load_dotenv("C://Users//ryanh//code//projects//canucksTix//.env")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="""Rank the following ticket listings for canucks games based on price and seat location: 
    1. Pair of tickets for tonight vs nyr, Sec 310 row 5, $180 per pair. Below face value.
    2. For Sale - 2 lower bowl tickets to Oct 28th game vs New York Rangers, Sec 122 row 11, $125 each
    3. I have two tickets for sale section 103 row 9. $220 per ticket. Jets shoot this way twice.
    Your output should be in JSON format. the keys should be the price, the location, and your rating (give it an excellent deal, good deal, face value, or bad deal)""",
    # config={
    #     "system_instruction": """ You are an incredibly smart ticket agent who can make an accurate estimation of a ticket's value for a Canucks game
    #     considering its price and seat location in Rogers Arena""",
    #     "temperature": 0.7,
    # },
)

print(response.text)


# keep your eyes out for free deals, links to other pages to sell tickets,
