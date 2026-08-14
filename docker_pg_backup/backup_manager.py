import os
import subprocess
import gzip
import shutil
import time
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

CONTAINER_NAME = os.getenv("CONTAINER_NAME")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
BACKUP_DIR = os.getenv("BACKUP_DIR", "./backups")
RETENTION_DAYS = int(os.getenv("RETENTION_DAYS", 7))

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    """Telegram bot orqali xabar yuborish"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"[!] Telegramga xabar yuborishda xatolik: {e}")

def cleanup_old_backups():
    """Belgilangan muddatdan eskirgan fayllarni o'chirish"""
    if not os.path.exists(BACKUP_DIR):
        return

    now = time.time()
    cutoff_time = now - (RETENTION_DAYS * 86400) # kunni soniyaga o'girish
    deleted_files = 0

    for filename in os.listdir(BACKUP_DIR):
        filepath = os.path.join(BACKUP_DIR, filename)
        if os.path.isfile(filepath):
            file_mtime = os.path.getmtime(filepath)
            if file_mtime < cutoff_time:
                os.remove(filepath)
                deleted_files += 1
                print(f"[*] Eski zaxira o'chirildi: {filename}")
    
    return deleted_files

def run_backup():
    """Docker ichidagi bazadan dump olish va arxivlash"""
    os.makedirs(BACKUP_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    sql_filename = f"{DB_NAME}_backup_{timestamp}.sql"
    gz_filename = f"{sql_filename}.gz"
    
    sql_filepath = os.path.join(BACKUP_DIR, sql_filename)
    gz_filepath = os.path.join(BACKUP_DIR, gz_filename)

    try:
        print(f"[*] Zaxira nusxa olinmoqda: {DB_NAME} (Konteyner: {CONTAINER_NAME})")
        
        # Docker exec orqali pg_dump buyrug'ini ishga tushirish
        dump_command = [
            "docker", "exec", "-t", CONTAINER_NAME,
            "pg_dump", "-U", DB_USER, DB_NAME
        ]
        
        with open(sql_filepath, "w") as out_file:
            subprocess.run(dump_command, stdout=out_file, check=True)

        print("[*] Arxivlanmoqda...")
        # SQL faylni GZIP formatida siqish
        with open(sql_filepath, 'rb') as f_in:
            with gzip.open(gz_filepath, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        os.remove(sql_filepath)
        
        file_size_mb = os.path.getsize(gz_filepath) / (1024 * 1024)
        
        deleted_count = cleanup_old_backups()

        # Muvaffaqiyatli xabar
        msg = (
            f"✅ <b>Baza zaxiralandi!</b>\n\n"
            f"<b>Baza:</b> {DB_NAME}\n"
            f"<b>Fayl:</b> {gz_filename}\n"
            f"<b>Hajmi:</b> {file_size_mb:.2f} MB\n"
            f"<b>O'chirilgan eski fayllar:</b> {deleted_count} ta"
        )
        print(msg)
        send_telegram_message(msg)

    except subprocess.CalledProcessError as e:
        error_msg = f"❌ <b>Zaxira olishda xatolik yuz berdi!</b>\nBaza: {DB_NAME}\nXato: Docker konteyner topilmadi yoki ulanishda muammo."
        print(error_msg)
        send_telegram_message(error_msg)
    except Exception as e:
        error_msg = f"❌ <b>Zaxira tizimida kutilmagan xatolik:</b>\n<code>{str(e)}</code>"
        print(error_msg)
        send_telegram_message(error_msg)

if __name__ == "__main__":
    run_backup()