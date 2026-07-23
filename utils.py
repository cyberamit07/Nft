import re
from datetime import datetime
import random
import string

# ========== USER STATES ==========
user_states = {}
temp_data = {}

# ========== VALIDATION ==========

def validate_username(username):
    """Validate Telegram username"""
    if not username:
        return False
    if username.startswith('@'):
        username = username[1:]
    # Telegram username: 5-32 characters, alphanumeric + underscore
    return bool(re.match(r'^[a-zA-Z0-9_]{5,32}$', username))

def validate_amount(amount):
    """Validate deal amount"""
    try:
        amount = float(amount)
        return amount >= 1.0 and amount <= 100000.0
    except:
        return False

def validate_currency(currency):
    """Validate currency"""
    valid_currencies = ["USD", "INR", "BTC", "ETH", "USDT", "BNB"]
    return currency.upper() in valid_currencies

# ========== FORMATTING ==========

def format_number(num):
    """Format number with commas"""
    if num is None:
        return "0"
    return f"{num:,.2f}"

def format_date(date_string):
    """Format date string"""
    if not date_string:
        return "N/A"
    try:
        dt = datetime.fromisoformat(date_string)
        return dt.strftime("%d-%b-%Y %I:%M %p")
    except:
        return date_string[:10]

def truncate_text(text, max_length=30):
    """Truncate long text"""
    if not text:
        return ""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

# ========== GENERATORS ==========

def generate_deal_code():
    """Generate random deal code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def generate_transaction_id():
    """Generate transaction reference"""
    return f"TXN-{''.join(random.choices(string.digits, k=6))}"

# ========== CALCULATIONS ==========

def calculate_fee(amount, fee_percent=0.5):
    """Calculate platform fee"""
    return amount * (fee_percent / 100)

def calculate_success_rate(total, successful):
    """Calculate success rate percentage"""
    if total == 0:
        return 0
    return (successful / total) * 100

# ========== PROGRESS BAR ==========

def progress_bar(percentage, length=10):
    """Create visual progress bar"""
    filled = int((percentage / 100) * length)
    empty = length - filled
    return f"▓" * filled + "░" * empty

# ========== EMOJI HELPERS ==========

def get_status_emoji(status):
    """Get emoji for deal status"""
    emojis = {
        'pending': '⏳',
        'paid': '💳',
        'confirmed': '✅',
        'released': '🔄',
        'disputed': '⚠️',
        'completed': '🎉',
        'rejected': '❌'
    }
    return emojis.get(status, '📌')

def get_rating_stars(rating):
    """Convert rating to stars"""
    if not rating:
        return "⭐" * 0
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    return "⭐" * full_stars + "✨" * half_star + "☆" * empty_stars

# ========== SECURITY ==========

def sanitize_input(text):
    """Sanitize user input"""
    if not text:
        return ""
    # Remove dangerous characters
    return re.sub(r'[<>&"\']', '', text)

def verify_admin(user_id, admin_ids):
    """Check if user is admin"""
    return user_id in admin_ids

# ========== MESSAGE HELPERS ==========

def split_long_message(text, max_length=4000):
    """Split long message for Telegram"""
    if len(text) <= max_length:
        return [text]
    
    parts = []
    lines = text.split('\n')
    current_part = ""
    
    for line in lines:
        if len(current_part) + len(line) + 1 <= max_length:
            current_part += line + "\n"
        else:
            parts.append(current_part)
            current_part = line + "\n"
    
    if current_part:
        parts.append(current_part)
    
    return parts

# ========== DATABASE HELPERS ==========

def get_user_display_name(user_data):
    """Get user's display name"""
    if not user_data:
        return "Unknown User"
    username = user_data[1]
    first_name = user_data[2]
    return f"@{username}" if username else first_name

def get_deal_summary(deal):
    """Get brief deal summary"""
    if not deal:
        return "No deal found"
    return f"#{deal[0]} | {deal[5]} {deal[6]} | {deal[8][:20]}"
