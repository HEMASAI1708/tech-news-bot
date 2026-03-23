import os
import requests
import google.generativeai as genai

# Get the key from GitHub's secret vault
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_news():
    print("Fetching news...")
    ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()[:5]
    news = ""
    for id in ids:
        item = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json").json()
        news += f"- {item['title']} (URL: {item.get('url', 'N/A')})\n"
    return news

def generate_post(news):
    model = genai.GenerativeModel('gemini-3-flash-preview')
    prompt = f"Write a professional, technical LinkedIn post for developers (NO EMOJIS) based on: {news}"
    return model.generate_content(prompt).text

if __name__ == "__main__":
    content = get_news()
    post = generate_post(content)
    print("--- POST GENERATED ---")
    print(post)