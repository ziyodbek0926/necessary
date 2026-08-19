Ushbu Python skripti Linux serverlarida (Ubuntu/Debian, CentOS) real vaqt rejimida xavfsizlik jurnallarini (`/var/log/auth.log` yoki `/var/log/secure`) kuzatib boradi. SSH orqali tizimga ruxsatsiz kirishga bo'lgan urinishlarni (Brute-force hujumlarini) avtomatik tarzda aniqlaydi va ma'lum bir chegaradan oshganda (masalan, 5 marta xato parol terilsa), hujumchining IP manzilini darhol tizim xavfsizlik devori (`iptables`) orqali bloklaydi.

## ✨ Asosiy xususiyatlari
* **Real-time Monitoring:** Jurnallarni xuddi `tail -f` buyrug'i kabi to'xtovsiz, uzilishlarsiz o'qiydi.
* **Regex Bilan Tahlil:** Noto'g'ri kiritilgan parollarni tezkor Regex naqshlari orqali aniq ajratib oladi.
* **Avtomatik Bloklash:** Inson aralashuvisiz tahdidlarni bartaraf etadi (`iptables` bilan integratsiya qilingan).
* **Oq Ro'yxat (Whitelist):** O'z IP manzilingizni yoki administratorlar guruhini tasodifiy bloklanishdan himoya qilish mexanizmi mavjud.
* **Kengaytirilgan Log yuritish:** Skript ishi va bloklangan IP'lar tarixi alohida `security_monitor.log` faylida saqlanadi.

## ⚙️ O'rnatish va Ishlatish

1. **Repozitoriyni yuklab oling:**

2. **Oq ro'yxatni (Whitelist) sozlang:**
   `whitelist.txt` fayliga kiring va bloklanmasligi kerak bo'lgan IP manzillarni (har birini yangi qatordan) kiriting.
   ```text
   127.0.0.1
   192.168.1.10
   ```

3. **Skriptni ishga tushiring:**
   Skript `iptables` bilan ishlagani va `/var/log` papkasini o'qigani uchun uni **root (sudo)** huquqlari bilan ishga tushirish majburiydir.
   ```bash
   sudo python3 analyzer.py
   ```

## 🛠 Texnologiyalar
* **Til:** Python (Built-in modullar: `re`, `subprocess`, `os`, `logging`)
* **OT va Tarmoq:** Linux, Iptables, SSH jurnallari
