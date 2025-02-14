from scapy.all import sniff, IP, TCP, conf
import re

# Используем уровень 3
conf.L3socket

# Функция для анализа пакетов
def analyze_packet(packet):
    print("[*] Packet received")  # Отладочный вывод
    if packet.haslayer(IP) and packet.haslayer(TCP):
        print("[*] TCP packet detected")  # Отладочный вывод
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        tcp_dport = packet[TCP].dport
        payload = str(packet[TCP].payload)

        # Поиск подозрительных активностей
        if tcp_dport in [22, 23, 80, 443]:
            if re.search(r"admin|password|login|root", payload, re.IGNORECASE):
                print(f"[!] Potential brute force attack detected from {ip_src} to {ip_dst}:{tcp_dport}")
                print(f"    Payload: {payload[:100]}...")

        # Поиск сканирования портов
        if tcp_dport > 1024 and "SYN" in str(packet[TCP].flags):
            print(f"[!] Potential port scan detected from {ip_src} to {ip_dst}:{tcp_dport}")

# Запуск сниффера
print("[*] Starting IDS...")
sniff(prn=analyze_packet, filter="tcp", count=0)  # Укажи нужный интерфейс