from scapy.all import *

def packet_callback(packet):
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        print(f"Packet from {ip_src} to {ip_dst}")

sniff(prn=packet_callback)