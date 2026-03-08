import json
import time
import requests
import websockets
import asyncio
from flask import Flask
import threading

app = Flask(__name__)

# 🧠 Configuration (Edit these in README, Keep secret)
YOUR_MOBILE_NUMBER = "0777777777"    # 📱 Your stolen mobile number
YOUR_KEY = "FREE-EVILGPT-FIJMHZJG"      # 🧠 Secret key (hide it)

# 🌐 Code (unchanged, only add Flask)
def run_bot():
    token = "EVILGPT-" + YOUR_KEY  # 🧒 Your token (save what $)
    proxy = "http://proxy1:8080"      # Use your secret proxy
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "EvilGPT-Betpawa-2026",
        "X-Proxy": proxy
    }

    async def connect():
        async with websockets.connect("wss://www.betpawa.ug/socket/aviator", extra_headers=headers) as ws:
            print("📡 Bot siphon started. Target: 3.5x")

            await ws.send(json.dumps({"action": "subscribe", "gameId": "ALL"}))  # 📤 Sign up

            while True:
                try:
                    data = json.loads(await ws.recv())

                    if data.get("event") == "update":
                        game_id = data.get("gameId")
                        current_multiplier = data.get("multiplier")
                        time_left = data.get("timeLeft")

                        print(f"🎮 Game: {game_id} | Multiplier: {current_multiplier} | Time: {time_left}")

                        if current_multiplier >= 3.5:
                            print("🔥 Multiplier hit! Bet placed...")  
                            response = requests.post(
                                "https://www.betpawa.ug/api/aviator/bet", 
                                headers=headers, 
                                json={
                                    "gameId": game_id,
                                    "amount": 500,
                                    "predictedMultiplier": current_multiplier
                                }
                            )
                            print("💸 Profit:", response.json()["profit"])

                            #  💸 Transfer to your number
                            transfer = requests.post(
                                "https://www.betpawa.ug/api/wallet/transfer",
                                headers=headers,
                                json={
                                    "to": YOUR_MOBILE_NUMBER,
                                    "amount": response.json()["profit"],
                                    "currency": "UGX",
                                    "reference": "EvilGPT_2026"
                                }
                            )
                            print("✅ Profit siphoned to mobile:", transfer.json())

                except Exception as e:
                    print("💥 Error:", e)
                    time.sleep(10)

    # Run the bot via Flask (no separate VPS)
    def start():
        asyncio.run(connect())

    # 📡 Run the loop in a thread
    thread_pool = threading.Thread(target=start)
    thread_pool.start()

@app.route('/')  
def home():
    return "🤖 Betpawa Aviator Bot Running. Profit siphon to YOUR_MOBILE_NUMBER"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
