import os
from dotenv import load_dotenv

load_dotenv()

# ========== BOT CONFIGURATION ==========
# ⚠️ IMPORTANT: Token ko secure rakhein!
# Naya token @BotFather se lena hai (publicly share na karein)

BOT_TOKEN = "8670451173:AAGje06r8DMxafuyaO6QKuLuM8ztG_oc3kA"  # <-- Yahan apna naya token daalein

ADMIN_IDS = [8603893462]  # Admin ID - @cyber_amit

BOT_NAME = "🛡️ PutNfts Escrow Bot"
CHANNEL_NAME = "PutNfts"  # @PutNfts
CHANNEL_LINK = "https://t.me/PutNfts"

DEVELOPER = "@cyber_amit"
DEVELOPER_LINK = "https://t.me/cyber_amit"

# ========== SUPPORTED CURRENCIES ==========
SUPPORTED_CURRENCIES = ["USD", "INR", "BTC", "ETH", "USDT", "BNB"]

# ========== DATABASE ==========
DATABASE_PATH = "data/escrow.db"

# ========== FEES ==========
PLATFORM_FEE_PERCENT = 0.5  # 0.5% platform fee
MIN_DEAL_AMOUNT = 1.0
MAX_DEAL_AMOUNT = 100000.0
