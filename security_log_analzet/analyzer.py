import time
import re
import subprocess
import os
from collections import defaultdict
import logging

LOG_FILE = "/var/log/auth.log"  # Ubuntu/Debian uchun SSH log fayli. CentOS/RHEL uchun: /var/log/secure
WHITELIST_FILE = "whitelist.txt"
MAX_FAILED_ATTEMPTS = 5         # Bloklash uchun nechta xato urinish kerakligi
BANNED_IPS = set()             

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("security_monitor.log"),
        logging.StreamHandler()
    ]
)

def load_whitelist():
    """Oq ro'yxatdagi (whitelist) IP manzillarni o'qish"""
    if not os.path.exists(WHITELIST_FILE):
        return set()
    with open(WHITELIST_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())

def block_ip(ip):
    """IP manzilni iptables orqali bloklash"""
    if ip in BANNED_IPS:
        return
    
    whitelist = load_whitelist()
    if ip in whitelist:
        logging.info(f"O'tkazib yuborildi (Whitelist): {ip}")
        return

    try:
        # Iptables orqali DROP qilish buyrug'i
        subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        BANNED_IPS.add(ip)
        logging.warning(f"🚨 IP bloklandi: {ip} (Brute-force hujum aniqlandi)")
    except subprocess.CalledProcessError as e:
        logging.error(f"IP ni bloklashda xatolik ({ip}): {e}")

def monitor_logs():
    """Real vaqt rejimida log faylni kuzatish (Tail -f kabi)"""
    failed_attempts = defaultdict(int)
    
    # "Failed password for root from 192.168.1.50 port 22 ssh2" kabi qatorlarni ushlash uchun Regex
    regex_pattern = re.compile(r"Failed password for (?:invalid user )?.*? from (\d+\.\d+\.\d+\.\d+)")

    if not os.path.exists(LOG_FILE):
        logging.error(f"Log fayl topilmadi: {LOG_FILE}. Root huquqida ekanligingizni tekshiring.")
        return

    logging.info(f"Kuzatuv boshlandi: {LOG_FILE}")
    
    with open(LOG_FILE, "r") as file:
        # Faylning eng oxiriga o'tish (faqat yangi xatolarni o'qish uchun)
        file.seek(0, os.SEEK_END)
        
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.5) # Yangi qator yozilishini kutish
                continue
            
            match = regex_pattern.search(line)
            if match:
                ip_address = match.group(1)
                failed_attempts[ip_address] += 1
                
                logging.info(f"Xato parol terildi: IP={ip_address} (Urinishlar soni: {failed_attempts[ip_address]})")
                
                if failed_attempts[ip_address] >= MAX_FAILED_ATTEMPTS:
                    block_ip(ip_address)

if __name__ == "__main__":
    # Root ruxsati borligini tekshirish (iptables ishlashi uchun kerak)
    if os.geteuid() != 0:
        logging.error("Skriptni ishga tushirish uchun root (sudo) huquqi talab qilinadi!")
    else:
        monitor_logs()