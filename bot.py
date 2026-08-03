# -*- coding: utf-8 -*-
"""
TELEGRAM BOT - HTOOL PREMIUM
Bot tự động trả lời và cung cấp Chat ID cho người dùng
Đã tích hợp Flask để chạy 24/7 trên Render miễn phí
"""

import requests
import time
import json
import os
import threading
from datetime import datetime
from flask import Flask

# ================== FLASK SERVER CHO RENDER ==================
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 HTOOL Premium Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# ================== CẤU HÌNH BOT ==================

# Lấy token từ biến môi trường (bảo mật hơn)
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8965450168:AAG8B6IaWTCGO8M5vPphqtA7jmFncxfeWk0")

# File lưu lịch sử người dùng
USERS_FILE = "bot_users.json"

# ================== HÀM GỬI TIN NHẮN ==================

def send_message(chat_id, text, parse_mode="HTML"):
    """Gửi tin nhắn đến người dùng"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"❌ Lỗi gửi tin nhắn: {e}")
        return None

def send_photo(chat_id, photo_url, caption=""):
    """Gửi ảnh đến người dùng"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    payload = {
        "chat_id": chat_id,
        "photo": photo_url,
        "caption": caption,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"❌ Lỗi gửi ảnh: {e}")
        return None

# ================== QUẢN LÝ NGƯỜI DÙNG ==================

def load_users():
    """Tải danh sách người dùng đã chat với bot"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_user(user_id, user_info):
    """Lưu thông tin người dùng"""
    users = load_users()
    user_id_str = str(user_id)
    
    if user_id_str not in users:
        users[user_id_str] = {
            "first_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_count": 0,
            **user_info
        }
    else:
        users[user_id_str]["last_seen"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        users[user_id_str]["message_count"] += 1
        users[user_id_str].update(user_info)
    
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)
    
    return users[user_id_str]

def get_user_count():
    """Đếm số người dùng đã chat với bot"""
    users = load_users()
    return len(users)

# ================== XỬ LÝ TIN NHẮN ==================

def handle_start(chat_id, user_info):
    """Xử lý lệnh /start"""
    first_name = user_info.get('first_name', 'Bạn')
    
    message = f"""👋 <b>Xin chào {first_name}!</b>

🤖 <b>Chào mừng đến với HTOOL PREMIUM Bot!</b>

━━━━━━━━━━━━━━━━━━━━
📱 <b>CHAT ID CỦA BẠN LÀ:</b>
<code>{chat_id}</code>
━━━━━━━━━━━━━━━━━━━━

📋 <b>HƯỚNG DẪN SỬ DỤNG:</b>

1️⃣ <b>Copy Chat ID</b> bên trên
2️⃣ <b>Mở tool HTOOL Premium</b>
3️⃣ <b>Vào phần cấu hình Telegram</b>
4️⃣ <b>Dán Chat ID</b> vào tool
5️⃣ <b>Bắt đầu nhận thông báo!</b>

━━━━━━━━━━━━━━━━━━━━

📌 <b>CÁC LỆNH HỖ TRỢ:</b>
/start - Xem Chat ID của bạn
/id - Xem Chat ID của bạn
/help - Hướng dẫn chi tiết
/info - Thông tin về bot
/contact - Liên hệ admin

━━━━━━━━━━━━━━━━━━━━

⚠️ <b>LƯU Ý:</b>
• Giữ Chat ID bí mật
• Không chia sẻ cho người khác
• Mỗi người có Chat ID riêng
• Chat ID này dùng để nhận thông báo riêng

💬 <b>Hỗ trợ:</b> @htool88
📞 <b>Zalo:</b> 0842010239"""

    send_message(chat_id, message)
    save_user(chat_id, user_info)
    print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] /start - {first_name} (ID: {chat_id})")


def handle_id(chat_id, user_info):
    """Xử lý lệnh /id"""
    first_name = user_info.get('first_name', 'Bạn')
    
    message = f"""📱 <b>CHAT ID CỦA BẠN:</b>

<code>{chat_id}</code>

👤 <b>Tên:</b> {first_name}
🆔 <b>ID:</b> <code>{chat_id}</code>

━━━━━━━━━━━━━━━━━━━━
📌 <b>Copy Chat ID này</b> và dán vào tool HTOOL Premium để nhận thông báo!
━━━━━━━━━━━━━━━━━━━━"""

    send_message(chat_id, message)
    save_user(chat_id, user_info)
    print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] /id - {first_name} (ID: {chat_id})")


def handle_help(chat_id, user_info):
    """Xử lý lệnh /help"""
    message = """📖 <b>HƯỚNG DẪN CHI TIẾT</b>

━━━━━━━━━━━━━━━━━━━━

<b>BƯỚC 1: LẤY CHAT ID</b>
• Chat /start hoặc /id
• Copy dãy số Chat ID

<b>BƯỚC 2: MỞ TOOL</b>
• Mở tool HTOOL Premium
• Vào game Chạy đua tốc độ (CDTD)
• Chọn cấu hình

<b>BƯỚC 3: CẤU HÌNH TELEGRAM</b>
• Chọn "Có" khi hỏi cấu hình Telegram
• Dán Chat ID đã copy
• Tool sẽ test kết nối

<b>BƯỚC 4: NHẬN THÔNG BÁO</b>
• Sau mỗi ván chơi, bot sẽ gửi kết quả
• Chỉ bạn mới xem được thông báo của mình
• Thông báo gồm: ván, cược, kết quả, lãi/lỗ...

━━━━━━━━━━━━━━━━━━━━

<b>CÁC LỆNH:</b>
/start - Bắt đầu
/id - Xem Chat ID
/help - Hướng dẫn này
/info - Thông tin bot
/stats - Thống kê bot
/contact - Liên hệ admin"""

    send_message(chat_id, message)
    save_user(chat_id, user_info)


def handle_info(chat_id, user_info):
    """Xử lý lệnh /info"""
    user_count = get_user_count()
    
    message = f"""🤖 <b>THÔNG TIN BOT</b>

━━━━━━━━━━━━━━━━━━━━
📌 <b>Tên bot:</b> HTOOL Premium Bot
🔧 <b>Phiên bản:</b> 3.0
👥 <b>Người dùng:</b> {user_count}
📅 <b>Hoạt động:</b> 24/7
━━━━━━━━━━━━━━━━━━━━

🎮 <b>HỖ TRỢ GAME:</b>
• Chạy đua tốc độ (CDTD)
• Vua thoát hiểm (VTH)

🔔 <b>TÍNH NĂNG:</b>
• Thông báo kết quả sau mỗi ván
• Thông báo riêng tư, bảo mật
• Hỗ trợ 40 thuật toán AI
• Tự động kiểm tra key

💬 <b>Liên hệ:</b> @htool88
📞 <b>Zalo:</b> 0842010239"""

    send_message(chat_id, message)
    save_user(chat_id, user_info)


def handle_contact(chat_id, user_info):
    """Xử lý lệnh /contact"""
    message = """📞 <b>LIÊN HỆ ADMIN</b>

━━━━━━━━━━━━━━━━━━━━
👤 <b>Admin:</b> Thành Công
📞 <b>Zalo:</b> 0842010239
💬 <b>Telegram:</b> @htool88
📱 <b>Nhóm Zalo:</b> https://zalo.me/g/fmyvre167
🔗 <b>Kênh Telegram:</b> https://t.me/+PByWNy8hDxYzYTRl
━━━━━━━━━━━━━━━━━━━━

⏰ <b>Hỗ trợ:</b> 8:00 - 22:00 hàng ngày
💡 <b>Mua key tool:</b> Liên hệ Zalo/Telegram"""

    send_message(chat_id, message)
    save_user(chat_id, user_info)


def handle_stats(chat_id, user_info):
    """Xử lý lệnh /stats"""
    user_count = get_user_count()
    users = load_users()
    
    today = datetime.now().strftime("%Y-%m-%d")
    today_users = sum(1 for u in users.values() if u.get('last_seen', '').startswith(today))
    
    message = f"""📊 <b>THỐNG KÊ BOT</b>

━━━━━━━━━━━━━━━━━━━━
👥 <b>Tổng người dùng:</b> {user_count}
📅 <b>Hôm nay:</b> {today_users} người dùng
🟢 <b>Trạng thái:</b> Đang hoạt động
⏰ <b>Uptime:</b> 24/7
━━━━━━━━━━━━━━━━━━━━

🤖 <b>HTOOL Premium v3.0</b>
🎮 <b>Hỗ trợ:</b> VTH + CDTD
🧠 <b>AI:</b> 40+ thuật toán"""

    send_message(chat_id, message)
    save_user(chat_id, user_info)


def handle_unknown(chat_id, user_info, text):
    """Xử lý tin nhắn không xác định"""
    first_name = user_info.get('first_name', 'Bạn')
    
    message = f"""🤔 <b>{first_name} à, tôi không hiểu lệnh của bạn!</b>

📋 <b>Các lệnh hỗ trợ:</b>
/start - Xem Chat ID của bạn
/id - Xem Chat ID của bạn
/help - Hướng dẫn chi tiết
/info - Thông tin về bot
/stats - Thống kê bot
/contact - Liên hệ admin

💡 <b>Bạn cần Chat ID?</b> Gửi /start nhé!"""

    send_message(chat_id, message)
    save_user(chat_id, user_info)


# ================== XỬ LÝ CHÍNH ==================

def process_message(msg):
    """Xử lý tin nhắn từ Telegram"""
    try:
        message = msg.get('message', {})
        if not message:
            return
        
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')
        user_info = {
            'first_name': message.get('from', {}).get('first_name', ''),
            'last_name': message.get('from', {}).get('last_name', ''),
            'username': message.get('from', {}).get('username', ''),
            'is_bot': message.get('from', {}).get('is_bot', False)
        }
        
        if not chat_id:
            return
        
        if text == '/start':
            handle_start(chat_id, user_info)
        elif text == '/id':
            handle_id(chat_id, user_info)
        elif text == '/help':
            handle_help(chat_id, user_info)
        elif text == '/info':
            handle_info(chat_id, user_info)
        elif text == '/contact':
            handle_contact(chat_id, user_info)
        elif text == '/stats':
            handle_stats(chat_id, user_info)
        else:
            handle_unknown(chat_id, user_info, text)
            
    except Exception as e:
        print(f"❌ Lỗi xử lý tin nhắn: {e}")


def get_updates(offset=None):
    """Lấy tin nhắn mới từ Telegram (Long Polling)"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {
        "timeout": 30,
        "limit": 10
    }
    if offset:
        params["offset"] = offset
    
    try:
        response = requests.get(url, params=params, timeout=35)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Lỗi API: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.Timeout:
        return None
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
        return None


def check_telegram_connection():
    """Kiểm tra kết nối đến Telegram API"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data.get('result', {})
                return True, bot_info
        return False, None
    except:
        return False, None


# ================== MAIN ==================

def main():
    """Hàm chính - Chạy bot"""
    print("=" * 60)
    print("🤖 HTOOL PREMIUM - TELEGRAM BOT")
    print("=" * 60)
    print()
    
    # Khởi động Flask server trong thread riêng
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Web server đã khởi động!")
    
    # Kiểm tra token
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ LỖI: Bạn chưa cấu hình BOT_TOKEN!")
        return
    
    print("🔍 Đang kiểm tra kết nối...")
    is_connected, bot_info = check_telegram_connection()
    
    if not is_connected:
        print("❌ Không thể kết nối đến Telegram API!")
        return
    
    print(f"✅ Kết nối thành công!")
    print(f"🤖 Bot: @{bot_info.get('username', 'Unknown')}")
    print(f"📅 Bắt đầu lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👥 Người dùng đã đăng ký: {get_user_count()}")
    print()
    print("🔄 Đang lắng nghe tin nhắn... (Ctrl+C để dừng)")
    print("=" * 60)
    print()
    
    last_update_id = 0
    
    while True:
        try:
            updates = get_updates(offset=last_update_id + 1)
            
            if updates and updates.get('ok') and updates.get('result'):
                for update in updates['result']:
                    update_id = update.get('update_id', 0)
                    if update_id > last_update_id:
                        last_update_id = update_id
                    
                    process_message(update)
            
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            print("\n\n👋 Bot đã dừng. Tạm biệt!")
            break
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            time.sleep(5)


# ================== KHỞI ĐỘNG ==================

def start_bot():
    """Khởi động bot trong thread riêng"""
    bot_thread = threading.Thread(target=main, daemon=True)
    bot_thread.start()
    print("🤖 Bot thread đã khởi động!")

# Tự động chạy khi deploy lên Render
start_bot()

if __name__ == "__main__":
    # Khi chạy local
    main()
