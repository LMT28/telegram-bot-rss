import requests
import feedparser
import time
import telegram

# === CONFIG ===
BOT_TOKEN = "8399865258:AAHfppcnl_tzUpu70i3KgCu-xSJ_13NTWEo"
CHAT_ID = "1737416591"
CHECK_INTERVAL = 300  # 5 menit (dalam detik)

# === RSS SOURCES ===
sources = {
    "Fabrizio Romano": "https://rss.app/feeds/0XhG4uwXxP2xGJfH.xml",  # RSS feed Fabrizio Romano Twitter/X
    "Sky Sports": "https://www.skysports.com/rss/12040",  # Sky Sports Football News
    "BBC Sport": "http://feeds.bbci.co.uk/sport/football/rss.xml?edition=uk",  # BBC Sport Football
    "Transfermarkt": "https://www.transfermarkt.com/rss/news"  # Transfermarkt News
}

# === Telegram Bot Setup ===
bot = telegram.Bot(token=BOT_TOKEN)

# === Store Sent Articles to Avoid Duplicates ===
sent_links = set()

def fetch_and_send():
    global sent_links
    for source, url in sources.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            if entry.link not in sent_links:
                # Simpan link supaya tidak dikirim ulang
                sent_links.add(entry.link)

                # Format pesan
                if "transfer" in entry.title.lower() or "rumour" in entry.title.lower() or "gossip" in entry.title.lower():
                    emoji = "🚨"
                else:
                    emoji = "💬"

                message = f"{emoji} *[{source}]* {entry.title}\n\n🔗 {entry.link}"
                bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

if __name__ == "__main__":
    print("InsideTheGoal Gossip Bot berjalan...")
    while True:
        fetch_and_send()
        time.sleep(CHECK_INTERVAL)
