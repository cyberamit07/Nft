import telebot
from telebot import types
import time
import logging
from datetime import datetime

from config import (
    BOT_TOKEN, ADMIN_IDS, BOT_NAME, CHANNEL_NAME, 
    CHANNEL_LINK, DEVELOPER, DEVELOPER_LINK,
    SUPPORTED_CURRENCIES, DATABASE_PATH, PLATFORM_FEE_PERCENT
)
from database import Database
from keyboards import *
from messages import *
from utils import *
import utils

# ========== SETUP ==========

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(BOT_TOKEN)
db = Database(DATABASE_PATH)

# ========== COMMAND HANDLERS ==========

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    first_name = message.from_user.first_name or "User"
    last_name = message.from_user.last_name or ""
    
    # Register user
    db.add_user(user_id, username, first_name, last_name)
    
    # Typing effect
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(0.5)
    
    # Send welcome with profile photo
    welcome_text = welcome_message(first_name)
    
    try:
        user_photos = bot.get_user_profile_photos(user_id, limit=1)
        if user_photos.total_count > 0:
            bot.send_photo(
                message.chat.id,
                user_photos.photos[0][-1].file_id,
                caption=welcome_text,
                reply_markup=main_menu_keyboard(),
                parse_mode='Markdown'
            )
        else:
            bot.send_message(
                message.chat.id,
                welcome_text,
                reply_markup=main_menu_keyboard(),
                parse_mode='Markdown'
            )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            welcome_text,
            reply_markup=main_menu_keyboard(),
            parse_mode='Markdown'
        )
    
    # Log
    logger.info(f"New user: {first_name} (@{username}) - {user_id}")
    
    # Delete start message
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

@bot.message_handler(commands=['admin', 'panel'])
def admin_panel_command(message):
    """Admin panel access"""
    user_id = message.from_user.id
    
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ *Unauthorized Access!*", parse_mode='Markdown')
        return
    
    stats = db.get_stats()
    admin_text = admin_stats_message(stats)
    
    bot.send_message(
        message.chat.id,
        admin_text,
        reply_markup=admin_main_keyboard(),
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['stats'])
def stats_command(message):
    """Quick stats command"""
    user_id = message.from_user.id
    user_data = db.get_user(user_id)
    
    if user_data:
        stats_text = stats_message(user_data)
        bot.reply_to(message, stats_text, parse_mode='Markdown')
    else:
        bot.reply_to(message, "📊 No stats available.", parse_mode='Markdown')

@bot.message_handler(commands=['help', 'support'])
def help_command(message):
    """Help command"""
    bot.reply_to(message, help_message(), parse_mode='Markdown')

@bot.message_handler(commands=['about'])
def about_command(message):
    """About command"""
    bot.reply_to(message, about_message(), parse_mode='Markdown')

# ========== CALLBACK HANDLERS ==========

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    try:
        # ===== MAIN MENU =====
        if call.data == "pending":
            deals = db.get_user_deals(user_id, status="pending")
            if not deals:
                bot.edit_message_text(
                    pending_deals_empty(),
                    chat_id,
                    message_id,
                    reply_markup=main_menu_keyboard(),
                    parse_mode='Markdown'
                )
            else:
                deal_text = f"📋 **Your Pending Deals** ({len(deals)})\n━━━━━━━━━━━━━━━━━━━━━\n\n"
                for deal in deals:
                    deal_text += f"""
{get_status_emoji(deal[6])} **#{deal[0]}** - `{deal[1]}`
💰 {deal[5]} {deal[6]}
👤 Seller: @{deal[4] or 'N/A'}
📦 {deal[8][:20]}
━━━━━━━━━━━━━━━━━━━━━
"""
                bot.edit_message_text(
                    deal_text,
                    chat_id,
                    message_id,
                    reply_markup=main_menu_keyboard(),
                    parse_mode='Markdown'
                )
        
        elif call.data == "stats":
            user_data = db.get_user(user_id)
            stats_text = stats_message(user_data) if user_data else "No stats available."
            bot.edit_message_text(
                stats_text,
                chat_id,
                message_id,
                reply_markup=main_menu_keyboard(),
                parse_mode='Markdown'
            )
        
        elif call.data == "history":
            deals = db.get_user_deals(user_id, limit=20)
            history_text = deal_history_message(deals)
            bot.edit_message_text(
                history_text,
                chat_id,
                message_id,
                reply_markup=main_menu_keyboard(),
                parse_mode='Markdown'
            )
        
        elif call.data == "create_deal":
            # Start deal creation flow
            bot.edit_message_text(
                "🆕 **Create New Deal**\n━━━━━━━━━━━━━━━━━━━━━\n\n"
                "📝 Please enter the *seller's username* (with @):\n\n"
                "💡 *Example:* @seller_username",
                chat_id,
                message_id,
                reply_markup=cancel_keyboard(),
                parse_mode='Markdown'
            )
            utils.user_states[user_id] = 'waiting_seller'
        
        elif call.data == "help":
            bot.edit_message_text(
                help_message(),
                chat_id,
                message_id,
                reply_markup=main_menu_keyboard(),
                parse_mode='Markdown'
            )
        
        elif call.data == "about":
            bot.edit_message_text(
                about_message(),
                chat_id,
                message_id,
                reply_markup=main_menu_keyboard(),
                parse_mode='Markdown'
            )
        
        elif call.data == "developer":
            developer_text = f"""
👨‍💼 **Developer Information**
━━━━━━━━━━━━━━━━━━━━━

🛠️ **Developer:** {DEVELOPER}
📌 **Channel:** {CHANNEL_LINK}
💬 **Contact:** {DEVELOPER_LINK}

━━━━━━━━━━━━━━━━━━━━━
⭐ *Support by joining our channel!*
"""
            bot.edit_message_text(
                developer_text,
                chat_id,
                message_id,
                reply_markup=main_menu_keyboard(),
                parse_mode='Markdown'
            )
        
        elif call.data == "back_main":
            user_data = db.get_user(user_id)
            first_name = user_data[2] if user_data else "User"
            bot.edit_message_text(
                welcome_message(first_name),
                chat_id,
                message_id,
                reply_markup=main_menu_keyboard(),
                parse_mode='Markdown'
            )
        
        elif call.data == "cancel":
            # Cancel current operation
            if user_id in utils.user_states:
                del utils.user_states[user_id]
            if user_id in utils.temp_data:
                del utils.temp_data[user_id]
            
            user_data = db.get_user(user_id)
            first_name = user_data[2] if user_data else "User"
            bot.edit_message_text(
                "✅ *Operation cancelled!*\n\n" + welcome_message(first_name),
                chat_id,
                message_id,
                reply_markup=main_menu_keyboard(),
                parse_mode='Markdown'
            )
        
        # ===== ADMIN CALLBACKS =====
        elif call.data.startswith("admin_"):
            if user_id not in ADMIN_IDS:
                bot.answer_callback_query(call.id, "⛔ Unauthorized!", show_alert=True)
                return
            
            if call.data == "admin_users":
                users = db.get_all_users()
                text = f"👥 **Total Users:** {len(users)}\n━━━━━━━━━━━━━━━━━━━━━\n\n"
                for user in users[:30]:
                    text += f"• @{user[1] or user[0]} - {user[5]} deals | ⭐ {user[8]:.1f}\n"
                bot.edit_message_text(
                    text,
                    chat_id,
                    message_id,
                    reply_markup=admin_main_keyboard(),
                    parse_mode='Markdown'
                )
            
            elif call.data == "admin_deals":
                deals = db.get_all_deals(limit=50)
                text = admin_deal_list(deals, "All Deals")
                bot.edit_message_text(
                    text,
                    chat_id,
                    message_id,
                    reply_markup=admin_main_keyboard(),
                    parse_mode='Markdown'
                )
            
            elif call.data == "admin_pending":
                deals = db.get_deals_by_status("pending", limit=50)
                text = admin_deal_list(deals, "Pending Deals")
                if deals:
                    text += "\n\n📌 *Use deal ID to take action*"
                bot.edit_message_text(
                    text,
                    chat_id,
                    message_id,
                    reply_markup=admin_main_keyboard(),
                    parse_mode='Markdown'
                )
            
            elif call.data == "admin_disputes":
                deals = db.get_deals_by_status("disputed", limit=50)
                text = admin_deal_list(deals, "Disputed Deals")
                bot.edit_message_text(
                    text,
                    chat_id,
                    message_id,
                    reply_markup=admin_main_keyboard(),
                    parse_mode='Markdown'
                )
            
            elif call.data == "admin_completed":
                deals = db.get_deals_by_status("completed", limit=50)
                text = admin_deal_list(deals, "Completed Deals")
                bot.edit_message_text(
                    text,
                    chat_id,
                    message_id,
                    reply_markup=admin_main_keyboard(),
                    parse_mode='Markdown'
                )
            
            elif call.data == "admin_stats":
                stats = db.get_stats()
                bot.edit_message_text(
                    admin_stats_message(stats),
                    chat_id,
                    message_id,
                    reply_markup=admin_main_keyboard(),
                    parse_mode='Markdown'
                )
            
            elif call.data == "admin_broadcast":
                bot.edit_message_text(
                    "📢 **Broadcast Message**\n━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "Please type the message you want to send to all users:\n\n"
                    "⚠️ *This will send to ALL bot users!*",
                    chat_id,
                    message_id,
                    reply_markup=types.InlineKeyboardMarkup().add(
                        types.InlineKeyboardButton("❌ Cancel", callback_data="back_main")
                    ),
                    parse_mode='Markdown'
                )
                utils.user_states[user_id] = 'waiting_broadcast'
        
        # ===== DEAL ACTIONS =====
        elif call.data.startswith("approve_"):
            deal_id = int(call.data.split('_')[1])
            db.update_deal_status(deal_id, 'confirmed')
            
            # Add transaction record
            deal = db.get_deal(deal_id)
            if deal:
                db.add_transaction(deal_id, deal[2], 'payment_confirmed', deal[5], deal[6])
            
            bot.answer_callback_query(call.id, "✅ Payment approved!", show_alert=True)
            bot.edit_message_text(
                f"✅ **Deal #{deal_id} status updated to 'Confirmed'**\n\n"
                f"📌 Seller can now deliver the item.",
                chat_id,
                message_id,
                reply_markup=admin_main_keyboard(),
                parse_mode='Markdown'
            )
        
        elif call.data.startswith("reject_"):
            deal_id = int(call.data.split('_')[1])
            bot.edit_message_text(
                f"❌ **Reject Deal #{deal_id}**\n━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Please type the reason for rejection:",
                chat_id,
                message_id,
                reply_markup=cancel_keyboard(),
                parse_mode='Markdown'
            )
            utils.user_states[user_id] = f'waiting_reject_{deal_id}'
        
        elif call.data.startswith("release_"):
            deal_id = int(call.data.split('_')[1])
            db.update_deal_status(deal_id, 'released')
            
            # Add transaction
            deal = db.get_deal(deal_id)
            if deal:
                db.add_transaction(deal_id, deal[2], 'funds_released', deal[5], deal[6])
                db.update_user_stats(deal[2], True)
                if deal[4]:
                    seller = db.get_user_by_username(deal[4])
                    if seller:
                        db.update_user_stats(seller[0], True)
            
            bot.answer_callback_query(call.id, "💰 Funds released!", show_alert=True)
            bot.edit_message_text(
                f"💰 **Deal #{deal_id} - Funds Released!**\n\n"
                f"✅ Seller has received the payment.\n"
                f"📌 Deal marked as 'Released'.",
                chat_id,
                message_id,
                reply_markup=admin_main_keyboard(),
                parse_mode='Markdown'
            )
        
        elif call.data.startswith("complete_"):
            deal_id = int(call.data.split('_')[1])
            db.update_deal_status(deal_id, 'completed')
            
            # Ask for rating
            bot.edit_message_text(
                f"🎉 **Deal #{deal_id} Completed!**\n━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"Please rate your experience:",
                chat_id,
                message_id,
                reply_markup=rating_keyboard(deal_id),
                parse_mode='Markdown'
            )
        
        elif call.data.startswith("dispute_"):
            deal_id = int(call.data.split('_')[1])
            bot.edit_message_text(
                f"⚠️ **Raise Dispute - Deal #{deal_id}**\n━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Please type the reason for dispute:",
                chat_id,
                message_id,
                reply_markup=cancel_keyboard(),
                parse_mode='Markdown'
            )
            utils.user_states[user_id] = f'waiting_dispute_{deal_id}'
        
        elif call.data.startswith("view_"):
            deal_id = int(call.data.split('_')[1])
            deal = db.get_deal(deal_id)
            if deal:
                deal_text = deal_status_message(deal)
                bot.edit_message_text(
                    deal_text,
                    chat_id,
                    message_id,
                    reply_markup=deal_admin_keyboard(deal_id) if user_id in ADMIN_IDS else main_menu_keyboard(),
                    parse_mode='Markdown'
                )
        
        elif call.data.startswith("upload_"):
            deal_id = int(call.data.split('_')[1])
            bot.edit_message_text(
                f"📤 **Upload Payment Proof - Deal #{deal_id}**\n━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Please send a **screenshot** of your payment:\n\n"
                "📸 Send as *Photo* or *Document*\n"
                "💰 Include transaction ID if possible\n\n"
                "⚠️ *File will be reviewed by admin*",
                chat_id,
                message_id,
                reply_markup=cancel_keyboard(),
                parse_mode='Markdown'
            )
            utils.user_states[user_id] = f'waiting_upload_{deal_id}'
        
        elif call.data.startswith("confirm_receipt_"):
            deal_id = int(call.data.split('_')[1])
            
            # Confirm receipt and complete deal
            db.update_deal_status(deal_id, 'completed')
            
            # Add transaction
            deal = db.get_deal(deal_id)
            if deal:
                db.add_transaction(deal_id, deal[2], 'confirmed_receipt', deal[5], deal[6])
            
            bot.answer_callback_query(call.id, "✅ Receipt confirmed!", show_alert=True)
            bot.edit_message_text(
                f"✅ **Receipt Confirmed - Deal #{deal_id}**\n━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🎉 Deal has been completed!\n\n"
                f"Please rate your experience:",
                chat_id,
                message_id,
                reply_markup=rating_keyboard(deal_id),
                parse_mode='Markdown'
            )
        
        elif call.data.startswith("raise_dispute_"):
            deal_id = int(call.data.split('_')[1])
            bot.edit_message_text(
                f"⚠️ **Raise Dispute - Deal #{deal_id}**\n━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Please type the reason for dispute in detail:\n\n"
                "📌 *Admin will review and take action*",
                chat_id,
                message_id,
                reply_markup=cancel_keyboard(),
                parse_mode='Markdown'
            )
            utils.user_states[user_id] = f'waiting_dispute_{deal_id}'
        
        elif call.data.startswith("rate_"):
            parts = call.data.split('_')
            deal_id = int(parts[1])
            rating = int(parts[2])
            
            # Update rating
            deal = db.get_deal(deal_id)
            if deal:
                # Rate seller if exists
                seller = db.get_user_by_username(deal[4])
                if seller:
                    db.update_rating(seller[0], rating)
            
            bot.answer_callback_query(call.id, f"⭐ Rated {rating}/5! Thank you!", show_alert=True)
            bot.edit_message_text(
                f"⭐ **Thank you for rating!**\n━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"You rated this deal {rating}/5 ⭐\n\n"
                f"🎉 Deal #{deal_id} is now complete!",
                chat_id,
                message_id,
                reply_markup=main_menu_keyboard(),
                parse_mode='Markdown'
            )
        
        # Acknowledge callback
        bot.answer_callback_query(call.id)
        
    except Exception as e:
        logger.error(f"Callback error: {e}")
        bot.answer_callback_query(call.id, "⚠️ Error processing request", show_alert=True)

# ========== MESSAGE HANDLERS ==========

@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text.strip()
    
    # Check if user is in a state
    if user_id in utils.user_states:
        state = utils.user_states[user_id]
        
        # ===== DEAL CREATION FLOW =====
        if state == 'waiting_seller':
            seller_username = text
            
            if not validate_username(seller_username):
                bot.reply_to(message, 
                    "⚠️ Invalid username! Please enter a valid Telegram username with @\n\n"
                    "💡 *Example:* @seller_username",
                    parse_mode='Markdown'
                )
                return
            
            # Store seller username
            utils.temp_data[user_id] = {'seller': seller_username}
            
            # Ask fo
