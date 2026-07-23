from telebot import types

# ========== MAIN KEYBOARDS ==========

def main_menu_keyboard():
    """Main dashboard keyboard for users"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("📋 My Pending Deals", callback_data="pending")
    btn2 = types.InlineKeyboardButton("📊 My Stats", callback_data="stats")
    btn3 = types.InlineKeyboardButton("📜 Deal History", callback_data="history")
    btn4 = types.InlineKeyboardButton("➕ Create New Deal", callback_data="create_deal")
    btn5 = types.InlineKeyboardButton("❓ Help & Support", callback_data="help")
    btn6 = types.InlineKeyboardButton("ℹ️ About", callback_data="about")
    btn7 = types.InlineKeyboardButton("👨‍💼 Contact Developer", callback_data="developer")
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    markup.add(btn7)
    
    return markup

# ========== ADMIN KEYBOARDS ==========

def admin_main_keyboard():
    """Admin main panel keyboard"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("👥 All Users", callback_data="admin_users")
    btn2 = types.InlineKeyboardButton("📋 All Deals", callback_data="admin_deals")
    btn3 = types.InlineKeyboardButton("⏳ Pending Approvals", callback_data="admin_pending")
    btn4 = types.InlineKeyboardButton("⚠️ Disputes", callback_data="admin_disputes")
    btn5 = types.InlineKeyboardButton("💰 Completed Deals", callback_data="admin_completed")
    btn6 = types.InlineKeyboardButton("📊 Bot Stats", callback_data="admin_stats")
    btn7 = types.InlineKeyboardButton("📢 Broadcast Message", callback_data="admin_broadcast")
    btn8 = types.InlineKeyboardButton("🔙 Back to Main", callback_data="back_main")
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    markup.add(btn7, btn8)
    
    return markup

def deal_admin_keyboard(deal_id):
    """Admin actions for a specific deal"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("✅ Approve Payment", callback_data=f"approve_{deal_id}")
    btn2 = types.InlineKeyboardButton("❌ Reject Payment", callback_data=f"reject_{deal_id}")
    btn3 = types.InlineKeyboardButton("🔄 Release Funds", callback_data=f"release_{deal_id}")
    btn4 = types.InlineKeyboardButton("✅ Confirm Completion", callback_data=f"complete_{deal_id}")
    btn5 = types.InlineKeyboardButton("⚠️ Mark Dispute", callback_data=f"dispute_{deal_id}")
    btn6 = types.InlineKeyboardButton("🔙 Back", callback_data="back_main")
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    
    return markup

# ========== DEAL KEYBOARDS ==========

def deal_action_keyboard(deal_id, user_role='buyer'):
    """Keyboard for deal participants"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    if user_role == 'buyer':
        btn1 = types.InlineKeyboardButton("📤 Upload Payment Proof", callback_data=f"upload_{deal_id}")
        btn2 = types.InlineKeyboardButton("✅ Confirm Receipt", callback_data=f"confirm_receipt_{deal_id}")
        btn3 = types.InlineKeyboardButton("⚠️ Raise Dispute", callback_data=f"raise_dispute_{deal_id}")
    else:
        btn1 = types.InlineKeyboardButton("📤 Upload Delivery Proof", callback_data=f"deliver_{deal_id}")
        btn2 = types.InlineKeyboardButton("⚠️ Raise Dispute", callback_data=f"raise_dispute_{deal_id}")
    
    btn3 = types.InlineKeyboardButton("🔍 View Deal Details", callback_data=f"view_{deal_id}")
    btn4 = types.InlineKeyboardButton("🔙 Back", callback_data="back_main")
    
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3, btn4)
    
    return markup

# ========== CONFIRMATION KEYBOARDS ==========

def confirm_keyboard(confirm_callback, cancel_callback):
    """Yes/No confirmation keyboard"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("✅ Yes", callback_data=confirm_callback)
    btn2 = types.InlineKeyboardButton("❌ Cancel", callback_data=cancel_callback)
    
    markup.add(btn1, btn2)
    return markup

def rating_keyboard(deal_id):
    """Rating keyboard for completed deals"""
    markup = types.InlineKeyboardMarkup(row_width=5)
    
    stars = []
    for i in range(1, 6):
        stars.append(types.InlineKeyboardButton(f"⭐ {i}", callback_data=f"rate_{deal_id}_{i}"))
    
    markup.add(*stars)
    
    btn_cancel = types.InlineKeyboardButton("🔙 Skip", callback_data="back_main")
    markup.add(btn_cancel)
    
    return markup

# ========== NAVIGATION ==========

def back_keyboard(callback="back_main"):
    """Simple back button"""
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Back", callback_data=callback))
    return markup

def cancel_keyboard():
    """Cancel keyboard"""
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("❌ Cancel", callback_data="cancel"))
    return markup
