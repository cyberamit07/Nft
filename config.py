import os
from dotenv import load_dotenv

load_dotenv()

# ========== BOT CONFIGURATION ==========
# Render pe environment variable se token lega

BOT_TOKEN = os.getenv("8670451173:AAGje06r8DMxafuyaO6QKuLuM8ztG_oc3kA")  # <-- Render pe set karna hai

ADMIN_IDS = [8603893462]
BOT_NAME = "🛡️ PutNfts Escrow Bot"
CHANNEL_NAME = "PutNfts"
CHANNEL_LINK = "https://t.me/PutNfts"
DEVELOPER = "@cyber_amit"
DEVELOPER_LINK = "https://t.me/cyber_amit"

# ========== DATABASE ==========
# Render pe persistent storage ke liye
import os
DATABASE_PATH = os.path.join(os.getcwd(), "data", "escrow.db")

# Ensure data directory exists
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
