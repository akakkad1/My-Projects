from google import genai
import os

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key="")

picks = []
os.system('clear')
surprise = input("Surprise me? (y/n): ")
if surprise.lower() == "y":
    picks.append("\nSurprise me!")
elif surprise.lower() == "n":
    genre = input("\nWhat type of genre of music do you want?: ")
    mood = input("What mood of music do you want?: ")
    other = input("Anything else? (ex. artist, language): ")
    picks += [genre, mood, other]


response = client.models.generate_content(
    model="gemini-3-flash-preview", contents=f"Give me a song in this format Song Name - Artist Name, based on these info {picks}"
)
print(response.text)
