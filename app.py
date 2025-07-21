from flask import Flask, render_template, request, jsonify, session
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    
    if "chat_history" not in session:
        session["chat_history"] = []

   
    session["chat_history"].append({"role": "user", "content": user_message})

   
    if "date" and "time" or"date and time" in user_message.lower():
        current_date = datetime.now().strftime("%B %d, %Y")
        current_time = datetime.now().strftime("%I:%M %p")
        return jsonify({"reply": f"Today's date and time is {current_date} and {current_time}"})
    elif "time" in user_message.lower():
        current_time = datetime.now().strftime("%I:%M %p")
        return jsonify({"reply": f"The current time is {current_time}"})

    elif "date" in user_message.lower():
        current_date = datetime.now().strftime("%B %d, %Y")
        return jsonify({"reply": f"Today's date is {current_date}"})
    
    
    elif "news" in user_message.lower():
        return jsonify({"reply": get_latest_news()})

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "JarvoBot"
    }

    messages = [{"role": "system", "content": "You are Jarvo, a friendly AI assistant."}] + session["chat_history"]

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": messages
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        assistant_reply = response.json()["choices"][0]["message"]["content"]
       
        session["chat_history"].append({"role": "assistant", "content": assistant_reply})
        return jsonify({"reply": assistant_reply})
    else:
        return jsonify({"reply": "⚠️ Something went wrong. Please try again."})



if __name__ == "__main__":
   app.run(host='0.0.0.0', port=10000, debug=True)

