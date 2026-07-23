from datetime import datetime

# ========== WELCOME & MAIN MESSAGES ==========

def welcome_message(first_name):
    return f"""
🌟 **Welcome, {first_name}!** 🌟

━━━━━━━━━━━━━━━━━━━━━
🛡️ **PutNfts Escrow Bot** 
━━━━━━━━━━━━━━━━━━━━━

✅ **Secure Escrow Services** for NFT deals
🔐 **100% Safe** transactions with admin verification
👨‍💼 **24/7 Admin Support** available

📌 *Channel:* [@PutNfts](https://t.me/PutNfts)

━━━━━━━━━━━━━━━━━━━━━
📌 *This is your Personal Deal Dashboard*
━━━━━━━━━━━━━━━━━━━━━

👇 *Select an option below* 👇
"""

def no_deals_found(username):
    return f"""
📭 **No Deals Found**

━━━━━━━━━━━━━━━━━━━━━
@{username} has not done any deal yet!

💡 *Start your first deal now using* ➕ *Create New Deal*
━━━━━━━━━━━━━━━━━━━━━
"""

def pending_deals_empty():
    return """
📭 **No Active/Pending Deals**

━━━━━━━━━━━━━━━━━━━━━
✨ *Your dashboard is clean!*

🚀 Start a new deal using ➕ *Create New Deal*
━━━━━━━━━━━━━━━━━━━━━
"""

# ========== DEAL MESSAGES ==========

def deal_created_message(deal_id, deal_code, buyer_username, seller_username, 
                         amount, currency, item_name):
    return f"""
🎉 **Deal Created Successfully!**
━━━━━━━━━━━━━━━━━━━━━

🆔 **Deal ID:** #{deal_id}
🔑 **Deal Code:** `{deal_code}`
👤 **Buyer:** @{buyer_username}
👤 **Seller:** @{seller_username}
💰 **Amount:** {amount} {currency}
📦 **Item:** {item_name}
📅 **Created:** {datetime.now().strftime('%d-%b-%Y %I:%M %p')}

━━━━━━━━━━━━━━━━━━━━━
⏳ *Status: Pending Payment*

📌 *Next Steps:*
1️⃣ Buyer sends payment to bot
2️⃣ Admin verifies the payment
3️⃣ Seller delivers the item
4️⃣ Buyer confirms receipt
5️⃣ Funds released to seller

━━━━━━━━━━━━━━━━━━━━━
🔒 *Your deal is secure with us!*
"""

def deal_status_message(deal):
    """Rich deal status display"""
    status_emoji = {
        'pending': '⏳',
        'paid': '💳',
        'confirmed': '✅',
        'released': '🔄',
        'disputed': '⚠️',
        'completed': '🎉',
        'rejected': '❌'
    }
    
    status_text = {
        'pending': 'Awaiting Payment',
        'paid': 'Payment Received - Awaiting Admin Confirmation',
        'confirmed': 'Payment Confirmed - Awaiting Delivery',
        'released': 'Funds Released - Awaiting Completion',
        'disputed': '⚠️ DISPUTED - Admin Review Required',
        'completed': '✅ COMPLETED - Deal Closed',
        'rejected': '❌ Rejected'
    }
    
    emoji = status_emoji.get(deal[6], '📌')
    status = status_text.get(deal[6], deal[6])
    
    return f"""
📋 **Deal Details**
━━━━━━━━━━━━━━━━━━━━━

🆔 **Deal #:** {deal[0]}
🔑 **Code:** `{deal[1]}`
👤 **Buyer:** {deal[2]}
👤 **Seller:** @{deal[4]}
💰 **Amount:** {deal[5]} {deal[6]}
💸 **Platform Fee:** {deal[7]} {deal[6]}
📦 **Item:** {deal[8]}
📝 **Description:** {deal[9] or 'N/A'}

━━━━━━━━━━━━━━━━━━━━━
{emoji} **Status:** {status}
📅 **Created:** {deal[11][:10] if deal[11] else 'N/A'}

━━━━━━━━━━━━━━━━━━━━━
"""

def deal_history_message(deals):
    if not deals:
        return no_deals_found("User")
    
    text = "📜 **Deal History**\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for deal in deals[:10]:
        status_emoji = {
            'pending': '⏳',
            'paid': '💳',
            'confirmed': '✅',
            'released': '🔄',
            'disputed': '⚠️',
            'completed': '🎉',
            'rejected': '❌'
        }.get(deal[6], '📌')
        
        text += f"""
{status_emoji} **#{deal[0]}** - `{deal[1]}`
💰 {deal[5]} {deal[6]}
📦 {deal[8][:20]}...
📅 {deal[11][:10] if deal[11] else 'N/A'}
━━━━━━━━━━━━━━━━━━━━━
"""
    
    return text

# ========== STATS MESSAGES ==========

def stats_message(user_data):
    """User statistics display"""
    if not user_data:
        return "📊 No stats available yet. Start your first deal!"
    
    user_id, username, first_name, last_name, joined_date, total_deals, successful_deals, failed_deals, rating, total_rating_count, is_banned, is_admin = user_data
    
    success_rate = 0
    if total_deals > 0:
        success_rate = (successful_deals / total_deals) * 100
    
    return f"""
📊 **Your Stats**
━━━━━━━━━━━━━━━━━━━━━

📌 *User:* @{username or first_name}
📅 *Member Since:* {joined_date[:10] if joined_date else 'N/A'}

━━━━━━━━━━━━━━━━━━━━━
📊 **Deal Statistics:**
📌 Total Deals: **{total_deals}**
✅ Successful: **{successful_deals}**
❌ Failed: **{failed_deals}**
📈 Success Rate: **{success_rate:.1f}%**

━━━━━━━━━━━━━━━━━━━━━
⭐ **Rating:** {rating:.1f} / 5.0
👤 **Total Ratings:** {total_rating_count}

━━━━━━━━━━━━━━━━━━━━━
🏆 *Keep up the great work!*
"""

# ========== ADMIN MESSAGES ==========

def admin_stats_message(stats):
    return f"""
🛡️ **PutNfts Escrow Bot - Admin Panel**
━━━━━━━━━━━━━━━━━━━━━

👋 Welcome *Admin* @cyber_amit!

━━━━━━━━━━━━━━━━━━━━━
📊 **Bot Statistics:**
━━━━━━━━━━━━━━━━━━━━━
👥 **Total Users:** {stats['total_users']}
📋 **Total Deals:** {stats['total_deals']}
⏳ **Pending:** {stats['pending_deals']}
✅ **Completed:** {stats['completed_deals']}
⚠️ **Disputes:** {stats['disputed_deals']}
💰 **Total Volume:** {stats['total_volume']:.2f} USD
💸 **Total Fees Earned:** {stats['total_fees']:.2f} USD

━━━━━━━━━━━━━━━━━━━━━
🔽 *Select an action below*
"""

def admin_deal_list(deals, title="Deals"):
    if not deals:
        return f"📋 No {title} found."
    
    text = f"📋 **{title}** ({len(deals)})\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for deal in deals[:20]:
        text += f"""
🆔 #{deal[0]} | `{deal[1]}`
💰 {deal[5]} {deal[6]} | {deal[8][:15]}
👤 @{deal[4] or 'N/A'} | {deal[6]}
━━━━━━━━━━━━━━━━━━━━━
"""
    
    return text

# ========== HELP MESSAGES ==========

def help_message():
    return f"""
❓ **Help & Support**
━━━━━━━━━━━━━━━━━━━━━

📌 *How Escrow Works:*

1️⃣ **Create Deal** - Buyer creates a deal with seller's username
2️⃣ **Make Payment** - Buyer sends payment to the bot
3️⃣ **Admin Verifies** - Our admin @cyber_amit confirms payment
4️⃣ **Seller Delivers** - Seller provides the product/service
5️⃣ **Buyer Confirms** - Buyer confirms receipt
6️⃣ **Funds Released** - Seller receives payment

━━━━━━━━━━━━━━━━━━━━━
🛡️ *Safety Tips:*
• Always verify admin usernames
• Never share OTP/password
• Keep screenshots of all payments
• Report suspicious activity immediately

━━━━━━━━━━━━━━━━━━━━━
📞 *Contact Admin:* @cyber_amit
📌 *Channel:* @PutNfts

━━━━━━━━━━━━━━━━━━━━━
⚡ *Response Time:* < 30 minutes
"""

def about_message():
    return f"""
ℹ️ **About PutNfts Escrow Bot**
━━━━━━━━━━━━━━━━━━━━━

🛡️ *Secure Escrow Service for NFT Transactions*
🔐 *100% Safe & Trusted*
👥 *Trusted by 1000+ NFT Enthusiasts*

━━━━━━━━━━━━━━━━━━━━━
📌 **Channel:** [@PutNfts](https://t.me/PutNfts)
👨‍💼 **Developer:** [@cyber_amit](https://t.me/cyber_amit)

━━━━━━━━━━━━━━━━━━━━━
✨ *Built with ❤️ for the NFT Community*
"""
