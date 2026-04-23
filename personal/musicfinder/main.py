from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key="AIzaSyDaQk614C6Wwn38L3hM0PXSgdL_Wp_vkbY")

picks = ["pop","2020s","happy"]
response = client.models.generate_content(
    model="gemini-3-flash-preview", contents=f"Give me a song in this format Song Name - Artist Name, based on these info {picks}"
)
print(response.text)
