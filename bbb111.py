import socket
import time

# Функция для отправки подозрительных пакетов
def send_suspicious_packet(target_ip, target_port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((target_ip, target_port))
        sock.sendall(b"GET /login?user=admin&password=123456 HTTP/1.1\r\n\r\n")
        print(f"[+] Sent suspicious packet to {target_ip}:{target_port}")
        sock.close()
    except Exception as e:
        print(f"[-] Failed to send packet to {target_ip}:{target_port}: {e}")

# Функция для сканирования портов
def port_scan(target_ip, start_port, end_port):
    for port in range(start_port, end_port + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                print(f"[+] Port {port} is open on {target_ip}")
            sock.close()
        except Exception as e:
            print(f"[-] Error scanning port {port}: {e}")

# Тестирование
if __name__ == "__main__":
    target_ip = "192.168.0.106"  # Замени на IP целевой машины
    target_port = 80  # HTTP порт

    # Имитация атаки подбора пароля
    print("[*] Simulating brute force attack...")
    send_suspicious_packet(target_ip, target_port)

    # Имитация сканирования портов
    print("[*] Simulating port scan...")
    port_scan(target_ip, 1, 1024)

    print("[*] Testing complete.")