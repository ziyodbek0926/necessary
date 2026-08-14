# Tarmoq Qurilmalarini Skanerlash va Inventarizatsiya Qilish Vositasi (Network Asset Discovery & Inventory Tool)

## Loyiha haqida
Ushbu loyiha tarmoqni avtomatik skanerlash, ARP so'rovlari orqali faol qurilmalarni aniqlash, ochiq portlarni tekshirish va AT (IT) auditlari uchun infratuzilma ma'lumotlarini to'g'ridan-to'g'ri PostgreSQL ma'lumotlar bazasiga saqlash uchun mo'ljallangan Python asosidagi CLI (Command Line Interface) vositasidir.

## Asosiy imkoniyatlari
* **Tezkor Skanerlash:** `scapy` kutubxonasi yordamida tarmoqdagi barcha qurilmalarni (IP va MAC manzillari bilan) tezkor ARP orqali aniqlash.
* **Portlarni Tekshirish:** Soketlar yordamida qurilmalardagi eng ko'p ishlatiladigan portlarni (SSH, HTTP, HTTPS, RDP) ochiq yoki yopiqligini tekshirish.
* **Ma'lumotlar Bazasi Integratsiyasi:** Topilgan barcha ma'lumotlarni xavfsiz va markazlashtirilgan holda saqlash uchun PostgreSQL bilan to'liq integratsiya.
* **CSV Eksport:** Skaner natijalarini hisobotlar va tahlillar uchun osonlik bilan CSV formatida yuklab olish.

## Talablar (Prerequisites)
Loyihani ishga tushirish uchun kompyuteringizda quyidagilar o'rnatilgan bo'lishi kerak:
* Python 3.8 yoki undan yuqori versiya
* PostgreSQL serveri
* Tarmoq paketlari (raw sockets) bilan ishlash uchun **root/administrator** ruxsati

## O'rnatish
Repozitoriyni yuklab oling:
   ```bash
   git clone [https://github.com/SizningUsername/network_inventory_tool.git](https://github.com/SizningUsername/network_inventory_tool.git)
   cd network_inventory_tool
   ```

## Faqat tarmoqni skanerlash va ekranga chiqarish:
```
sudo python net_scanner.py -t 192.168.1.0/24
```

## Skaner qilish va bazaga yozish, hamda CSV ga olish:
```
Skaner qilish va bazaga yozish, hamda CSV ga olish:
```