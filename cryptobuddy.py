# -------------------------------
# CryptoBuddy: NLP + Real-Time CoinGecko Data
# -------------------------------

import requests
import nltk
from nltk.tokenize import word_tokenize
import nltk
nltk.download("punkt")
nltk.download("punkt_tab")
# Download tokenizer (only needed once)
nltk.download('punkt')

# -------------------------------
# Sample Sustainability Dataset
# (Because CoinGecko does not provide energy-use data)
# -------------------------------
sustainability_db = {
    "bitcoin": {"energy_use": "high", "sustainability_score": 3/10},
    "ethereum": {"energy_use": "medium", "sustainability_score": 6/10},
    "cardano": {"energy_use": "low", "sustainability_score": 8/10}
}

# -------------------------------
# Fetch Real-Time Coin Data
# -------------------------------
def fetch_coin_data(coin_id="bitcoin", days=30):
    """Fetch real-time price, market cap, and volume from CoinGecko"""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    
    data = r.json()
    market_data = data.get("market_data", {})
    
    return {
        "coin_id": coin_id,
        "name": data.get("name", coin_id.capitalize()),
        "last_price": market_data.get("current_price", {}).get("usd", 0),
        "market_cap": market_data.get("market_cap", {}).get("usd", 0),
        "volume": market_data.get("total_volume", {}).get("usd", 0)
    }

# -------------------------------
# Rule-Based Analysis
# -------------------------------
def analyze_coin(coin_id):
    """Analyze profitability + sustainability of a coin"""
    coin_data = fetch_coin_data(coin_id)
    if not coin_data:
        return None
    
    price = coin_data["last_price"]
    market_cap = coin_data["market_cap"]
    volume = coin_data["volume"]

    # Profitability heuristic: liquidity ratio
    liquidity_ratio = volume / market_cap if market_cap else 0
    if liquidity_ratio > 0.1:
        profitability = "High"
    elif liquidity_ratio > 0.05:
        profitability = "Medium"
    else:
        profitability = "Low"
    
    # Sustainability from static dataset
    sustain = sustainability_db.get(coin_id, {"energy_use": "unknown", "sustainability_score": 0.5})
    sustainability = f"{sustain['sustainability_score']*10}/10 ({sustain['energy_use']} energy use)"
    
    return {
        "name": coin_data["name"],
        "price": price,
        "market_cap": market_cap,
        "volume": volume,
        "profitability": profitability,
        "sustainability": sustainability
    }

# -------------------------------
# NLP Intent Matching
# -------------------------------
def classify_intent(user_query):
    tokens = [t.lower() for t in word_tokenize(user_query)]

    # Synonym groups
    sustainability_keywords = {"sustainable", "eco", "green", "environment", "planet", "friendly"}
    profit_keywords = {"profit", "profitable", "gain", "investment", "money", "rich"}
    trend_keywords = {"trend", "trending", "up", "rise", "growing", "increase"}
    
    if any(word in tokens for word in sustainability_keywords):
        return "sustainability"
    elif any(word in tokens for word in profit_keywords):
        return "profitability"
    elif any(word in tokens for word in trend_keywords):
        return "trend"
    elif "bitcoin" in tokens:
        return "bitcoin"
    elif "ethereum" in tokens:
        return "ethereum"
    elif "cardano" in tokens:
        return "cardano"
    else:
        return "unknown"

# -------------------------------
# Chatbot Conversation Flow
# -------------------------------
def chatbot():
    print("🤖 Hi, I’m CryptoBuddy! 🌍💰")
    print("I fetch live market data from CoinGecko + sustainability insights.")
    print("Ask me about Bitcoin, Ethereum, Cardano, trends, sustainability, or profitability.")
    print("Type 'quit' anytime to exit.\n")

    while True:
        user_query = input("You: ")
        if user_query.lower() in ["quit", "exit", "bye"]:
            print("CryptoBuddy: Goodbye! ⚠️ Remember, crypto is risky — always do your own research (DYOR)!")
            break

        intent = classify_intent(user_query)

        if intent in ["bitcoin", "ethereum", "cardano"]:
            result = analyze_coin(intent)
            if result:
                print(f"\nCryptoBuddy: 🔎 {result['name']}")
                print(f"  Price: ${result['price']:.2f}")
                print(f"  Market Cap: ${result['market_cap']:,}")
                print(f"  Volume: ${result['volume']:,}")
                print(f"  Profitability: {result['profitability']}")
                print(f"  Sustainability: {result['sustainability']}")
            else:
                print("CryptoBuddy: ❌ Could not fetch data, try again later.")

        elif intent == "sustainability":
            best_coin = max(sustainability_db, key=lambda x: sustainability_db[x]["sustainability_score"])
            result = analyze_coin(best_coin)
            print(f"CryptoBuddy: 🌱 The greenest coin is {result['name']} "
                  f"with sustainability {result['sustainability']}.")

        elif intent == "profitability":
            # Check which has highest liquidity ratio
            scores = {}
            for coin in sustainability_db.keys():
                result = analyze_coin(coin)
                if result:
                    scores[coin] = result
            best = max(scores.values(), key=lambda x: x["profitability"])
            print(f"CryptoBuddy: 💰 The most profitable pick looks like {best['name']} "
                  f"(Profitability: {best['profitability']}).")

        elif intent == "trend":
            print("CryptoBuddy: 📈 I currently check profitability trends via volume/market cap. "
                  "Try asking about a specific coin like Bitcoin or Ethereum!")

        else:
            print("CryptoBuddy: 🤷 I didn’t quite get that. Try asking about Bitcoin, Ethereum, Cardano, "
                  "or use words like 'green', 'profit', or 'trending'.")

        # Always end with disclaimer
        print("⚠️ Crypto is risky — always do your own research (DYOR)!\n")

# -------------------------------
# Run Chatbot
# -------------------------------
chatbot()
