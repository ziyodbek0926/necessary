# Docker PostgreSQL Avtomatik Zaxira Boshqaruvchisi (Automated Backup Manager)

## Loyiha haqida
Ushbu skript Docker konteynerida aylanayotgan PostgreSQL ma'lumotlar bazasidan avtomatik ravishda `pg_dump` oladi, uni GZIP formatida siqadi (xotirani tejash uchun) va jarayon natijasi (fayl hajmi, holati) haqida Telegram bot orqali xabar yuboradi. Shuningdek, server xotirasi to'lib qolmasligi uchun belgilangan muddatdan (masalan, 7 kundan) eskirgan zaxira fayllarini avtomatik tozalaydi.

## Asosiy imkoniyatlari
* ** Docker Integratsiyasi:** Konteyner ichidagi bazaga tashqaridan to'g'ridan-to'g'ri ulanib, ishonchli nusxa oladi.
* ** Ma'lumotlarni Siqish:** Zaxira qilingan SQL fayllarni avtomatik tarzda `.gz` formatiga o'tkazib, disk hajmini tejaydi.
* ** Telegram Xabarnomalar (Alerting):** Jarayon muvaffaqiyatli o'tdimi yoki xatolik yuz berdimi — barchasi haqida bot orqali xabar yuboradi.
* ** Xotirani Boshqarish:** Eski zaxira nusxalarini avtomatik o'chirish logikasi mavjud (Retention policy).

## O'rnatish va Ishga tushirish

1. **Repozitoriyni yuklab oling va papkaga kiring:**
   ```bash
   git clone https://github.com/SizningUsername/docker_pg_backup.git
   cd docker_pg_backup
   ```

2. **Muhit o'zgaruvchilari faylini yarating va tahrirlang:**
   ```bash
   cp .env.example .env
   nano .env
   ```
   *(Ichiga konteyner nomi, baza nomi va Telegram bot tokeningizni kiriting)*

3. **Kutubxonalarni o'rnating:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Skriptni qo'lda sinab ko'rish uchun ishga tushiring:**
   ```bash
   python backup_manager.py
   ```

## Cron yordamida avtomatlashtirish (Har kuni tungi soat 02:00 da)
Serverda skriptni har kuni avtomatik ishlashi uchun crontab'ga qo'shing:

```bash
crontab -e
```
Quyidagi qatorni qo'shing (yo'llarni o'zingizga moslashtiring):
```text
0 2 * * * cd /path/to/docker_pg_backup && /usr/bin/python3 backup_manager.py >> /var/log/pg_backup.log 2>&1
```

## Texnologiyalar Steki
* **Python** (Subprocess, Shutil, OS, Requests)
* **Docker & PostgreSQL**
* **Telegram Bot API**