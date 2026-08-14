import argparse
import socket
import csv
from datetime import datetime
import psycopg2
from scapy.all import ARP, Ether, srp

# Ma'lumotlar bazasi sozlamalari
DB_CONFIG = {
    "dbname": "inventory_db",
    "user": "postgres",
    "password": "yourpassword",
    "host": "localhost",
    "port": "5432"
}

class NetworkScanner:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.devices = []

    def scan_network(self):
        print(f"[*] {self.target_ip} tarmog'i skaner qilinmoqda...")
        arp = ARP(pdst=self.target_ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp

        result = srp(packet, timeout=3, verbose=0)[0]

        for sent, received in result:
            device = {
                'ip': received.psrc,
                'mac': received.hwsrc,
                'open_ports': self.scan_ports(received.psrc)
            }
            self.devices.append(device)
            print(f"[+] Qurilma topildi: IP={device['ip']}, MAC={device['mac']}")
        
        return self.devices

    def scan_ports(self, ip):
        # Eng ko'p ishlatiladigan portlar (SSH, HTTP, HTTPS, RDP)
        ports = [22, 80, 443, 3389]
        open_ports = []
        
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(str(port))
            sock.close()
        
        return ",".join(open_ports) if open_ports else "None"


class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.config)
            self.create_table()
        except Exception as e:
            print(f"[!] Bazaga ulanishda xatolik: {e}")

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS network_devices (
            id SERIAL PRIMARY KEY,
            ip_address VARCHAR(15),
            mac_address VARCHAR(17),
            open_ports VARCHAR(50),
            scan_time TIMESTAMP
        );
        """
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()

    def save_devices(self, devices):
        if not self.conn:
            return
            
        query = """
        INSERT INTO network_devices (ip_address, mac_address, open_ports, scan_time)
        VALUES (%s, %s, %s, %s)
        """
        with self.conn.cursor() as cur:
            for dev in devices:
                cur.execute(query, (dev['ip'], dev['mac'], dev['open_ports'], datetime.now()))
        self.conn.commit()
        print(f"[*] {len(devices)} ta qurilma ma'lumotlar bazasiga saqlandi.")

    def close(self):
        if self.conn:
            self.conn.close()


def export_to_csv(devices, filename="inventory.csv"):
    keys = devices[0].keys() if devices else []
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(devices)
    print(f"[*] Natijalar {filename} fayliga saqlandi.")


def main():
    parser = argparse.ArgumentParser(description="Tarmoq va qurilmalarni inventarizatsiya qiluvchi CLI vosita.")
    parser.add_argument("-t", "--target", required=True, help="Maqsadli IP yoki Subnet (masalan: 192.168.1.0/24)")
    parser.add_argument("--csv", action="store_true", help="Natijalarni CSV faylga eksport qilish")
    parser.add_argument("--db", action="store_true", help="Natijalarni PostgreSQL bazasiga saqlash")
    args = parser.parse_args()

    scanner = NetworkScanner(args.target)
    devices = scanner.scan_network()

    if not devices:
        print("[-] Tarmoqda hech qanday faol qurilma topilmadi.")
        return

    if args.csv:
        export_to_csv(devices)

    if args.db:
        db = DatabaseManager(DB_CONFIG)
        db.connect()
        db.save_devices(devices)
        db.close()


if __name__ == "__main__":
    main()