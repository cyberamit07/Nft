import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_path="data/escrow.db"):
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Create all necessary tables"""
        
        # Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                joined_date TEXT,
                total_deals INTEGER DEFAULT 0,
                successful_deals INTEGER DEFAULT 0,
                failed_deals INTEGER DEFAULT 0,
                rating REAL DEFAULT 0.0,
                total_rating_count INTEGER DEFAULT 0,
                is_banned BOOLEAN DEFAULT FALSE,
                is_admin BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Deals table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS deals (
                deal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                deal_code TEXT UNIQUE,
                buyer_id INTEGER,
                seller_id INTEGER,
                seller_username TEXT,
                amount REAL,
                currency TEXT,
                platform_fee REAL,
                item_name TEXT,
                item_description TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT,
                paid_at TEXT,
                confirmed_at TEXT,
                released_at TEXT,
                completed_at TEXT,
                disputed_at TEXT,
                dispute_reason TEXT,
                dispute_resolved BOOLEAN DEFAULT FALSE,
                admin_notes TEXT,
                FOREIGN KEY (buyer_id) REFERENCES users(user_id),
                FOREIGN KEY (seller_id) REFERENCES users(user_id)
            )
        ''')
        
        # Transactions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                tx_id INTEGER PRIMARY KEY AUTOINCREMENT,
                deal_id INTEGER,
                user_id INTEGER,
                type TEXT,
                amount REAL,
                currency TEXT,
                timestamp TEXT,
                screenshot_file_id TEXT,
                screenshot_unique_id TEXT,
                notes TEXT,
                FOREIGN KEY (deal_id) REFERENCES deals(deal_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Messages table (for tracking bot messages)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bot_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message_id INTEGER,
                chat_id INTEGER,
                created_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Settings table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT
            )
        ''')
        
        self.conn.commit()
    
    # ========== USER OPERATIONS ==========
    
    def add_user(self, user_id, username, first_name, last_name=None):
        joined_date = datetime.now().isoformat()
        self.cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, joined_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, joined_date))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def get_user(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()
    
    def get_user_by_username(self, username):
        if username.startswith('@'):
            username = username[1:]
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone()
    
    def update_user_stats(self, user_id, successful=True):
        if successful:
            self.cursor.execute('''
                UPDATE users 
                SET total_deals = total_deals + 1, 
                    successful_deals = successful_deals + 1 
                WHERE user_id = ?
            ''', (user_id,))
        else:
            self.cursor.execute('''
                UPDATE users 
                SET total_deals = total_deals + 1, 
                    failed_deals = failed_deals + 1 
                WHERE user_id = ?
            ''', (user_id,))
        self.conn.commit()
    
    def update_rating(self, user_id, rating):
        self.cursor.execute('''
            UPDATE users 
            SET rating = (rating * total_rating_count + ?) / (total_rating_count + 1),
                total_rating_count = total_rating_count + 1
            WHERE user_id = ?
        ''', (rating, user_id))
        self.conn.commit()
    
    def get_all_users(self):
        self.cursor.execute('SELECT * FROM users ORDER BY total_deals DESC')
        return self.cursor.fetchall()
    
    # ========== DEAL OPERATIONS ==========
    
    def generate_deal_code(self):
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    def create_deal(self, buyer_id, seller_username, amount, currency, item_name, item_description=""):
        deal_code = self.generate_deal_code()
        created_at = datetime.now().isoformat()
        platform_fee = amount * 0.005  # 0.5% fee
        
        self.cursor.execute('''
            INSERT INTO deals (
                deal_code, buyer_id, seller_username, amount, currency, 
                platform_fee, item_name, item_description, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (deal_code, buyer_id, seller_username, amount, currency, 
              platform_fee, item_name, item_description, created_at))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_deal(self, deal_id):
        self.cursor.execute('SELECT * FROM deals WHERE deal_id = ?', (deal_id,))
        return self.cursor.fetchone()
    
    def get_deal_by_code(self, deal_code):
        self.cursor.execute('SELECT * FROM deals WHERE deal_code = ?', (deal_code,))
        return self.cursor.fetchone()
    
    def get_user_deals(self, user_id, status=None, limit=50):
        if status:
            self.cursor.execute('''
                SELECT * FROM deals 
                WHERE (buyer_id = ? OR seller_username = ?) AND status = ?
                ORDER BY deal_id DESC LIMIT ?
            ''', (user_id, user_id, status, limit))
        else:
            self.cursor.execute('''
                SELECT * FROM deals 
                WHERE buyer_id = ? OR seller_username = ?
                ORDER BY deal_id DESC LIMIT ?
            ''', (user_id, user_id, limit))
        return self.cursor.fetchall()
    
    def get_deals_by_status(self, status, limit=100):
        self.cursor.execute('''
            SELECT * FROM deals 
            WHERE status = ?
            ORDER BY deal_id DESC LIMIT ?
        ''', (status, limit))
        return self.cursor.fetchall()
    
    def get_all_deals(self, limit=200):
        self.cursor.execute('SELECT * FROM deals ORDER BY deal_id DESC LIMIT ?', (limit,))
        return self.cursor.fetchall()
    
    def update_deal_status(self, deal_id, status):
        timestamp = datetime.now().isoformat()
        status_map = {
            'paid': 'paid_at',
            'confirmed': 'confirmed_at',
            'released': 'released_at',
            'completed': 'completed_at',
            'disputed': 'disputed_at'
        }
        
        if status in status_map:
            self.cursor.execute(f'''
                UPDATE deals 
                SET status = ?, {status_map[status]} = ?
                WHERE deal_id = ?
            ''', (status, timestamp, deal_id))
        else:
            self.cursor.execute('''
                UPDATE deals SET status = ? WHERE deal_id = ?
            ''', (status, deal_id))
        self.conn.commit()
    
    def update_deal_seller(self, deal_id, seller_id):
        self.cursor.execute('''
            UPDATE deals SET seller_id = ? WHERE deal_id = ?
        ''', (seller_id, deal_id))
        self.conn.commit()
    
    def add_dispute(self, deal_id, reason):
        self.cursor.execute('''
            UPDATE deals 
            SET dispute_reason = ?, disputed_at = ?, status = 'disputed'
            WHERE deal_id = ?
        ''', (reason, datetime.now().isoformat(), deal_id))
        self.conn.commit()
    
    def resolve_dispute(self, deal_id, resolution, notes=""):
        self.cursor.execute('''
            UPDATE deals 
            SET dispute_resolved = TRUE, 
                status = ?,
                admin_notes = COALESCE(admin_notes || ' | ', '') || ?
            WHERE deal_id = ?
        ''', (resolution, notes, deal_id))
        self.conn.commit()
    
    # ========== TRANSACTION OPERATIONS ==========
    
    def add_transaction(self, deal_id, user_id, tx_type, amount, currency, 
                        screenshot_file_id=None, screenshot_unique_id=None, notes=""):
        self.cursor.execute('''
            INSERT INTO transactions 
            (deal_id, user_id, type, amount, currency, timestamp, 
             screenshot_file_id, screenshot_unique_id, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (deal_id, user_id, tx_type, amount, currency, 
              datetime.now().isoformat(), screenshot_file_id, 
              screenshot_unique_id, notes))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_transactions(self, deal_id):
        self.cursor.execute('''
            SELECT * FROM transactions WHERE deal_id = ? ORDER BY tx_id ASC
        ''', (deal_id,))
        return self.cursor.fetchall()
    
    # ========== MESSAGE TRACKING ==========
    
    def save_message(self, user_id, message_id, chat_id):
        self.cursor.execute('''
            INSERT INTO bot_messages (user_id, message_id, chat_id, created_at)
            VALUES (?, ?, ?, ?)
        ''', (user_id, message_id, chat_id, datetime.now().isoformat()))
        self.conn.commit()
    
    def get_user_messages(self, user_id, limit=10):
        self.cursor.execute('''
            SELECT * FROM bot_messages 
            WHERE user_id = ?
            ORDER BY id DESC LIMIT ?
        ''', (user_id, limit))
        return self.cursor.fetchall()
    
    # ========== STATISTICS ==========
    
    def get_stats(self):
        stats = {}
        
        self.cursor.execute('SELECT COUNT(*) FROM users')
        stats['total_users'] = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM deals')
        stats['total_deals'] = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM deals WHERE status = "pending"')
        stats['pending_deals'] = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM deals WHERE status = "completed"')
        stats['completed_deals'] = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM deals WHERE status = "disputed"')
        stats['disputed_deals'] = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT SUM(amount) FROM deals WHERE status = "completed"')
        result = self.cursor.fetchone()[0]
        stats['total_volume'] = result or 0
        
        self.cursor.execute('SELECT SUM(platform_fee) FROM deals WHERE status = "completed"')
        result = self.cursor.fetchone()[0]
        stats['total_fees'] = result or 0
        
        return stats
    
    def close(self):
        self.conn.close()
