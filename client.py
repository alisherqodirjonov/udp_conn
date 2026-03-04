import socket
import sys
import time
import random
import string
from datetime import datetime

PAYLOAD_SIZE = 200   # bytes per packet

def generate_random_payload(size=200):
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=size)).encode()

# Parse argument (supports both formats)
if len(sys.argv) < 2:
    print("Usage:")
    print("   python3 client.py <server_ip>:<port>")
    print("or python3 client.py <server_ip> <port>")
    print("Example: python3 client.py 127.0.0.1:12345")
    sys.exit(1)

try:
    if ':' in sys.argv[1]:
        server_ip, port_str = sys.argv[1].split(':', 1)
        port = int(port_str)
    else:
        server_ip = sys.argv[1]
        port = int(sys.argv[2])
except:
    print("Error: Invalid IP:port format")
    sys.exit(1)

server_addr = (server_ip, port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"[{datetime.now().strftime('%H:%M:%S')}] UDP Client started")
print(f"Sending to {server_ip}:{port}")
print("Press Ctrl+C to stop\n")

packets_sent = 0
packets_received = 0
start_time = time.time()

try:
    while True:
        # Send random payload
        payload = generate_random_payload(PAYLOAD_SIZE)
        sock.sendto(payload, server_addr)
        packets_sent += 1
        
        # Try to receive reply
        try:
            sock.settimeout(0.1)
            data, addr = sock.recvfrom(4096)
            packets_received += 1
        except socket.timeout:
            pass
        
        # Show live stats every 5 seconds
        elapsed = time.time() - start_time
        if int(elapsed) % 5 == 0 and int(elapsed) > 0:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ↑ Sent: {packets_sent} | ↓ Received: {packets_received} | "
                  f"Rate: {packets_sent/elapsed:.1f} pkt/s", end="\r")
        
        time.sleep(0.05)   # ~20 packets per second

except KeyboardInterrupt:
    print("\n\nClient stopped by user (Ctrl+C)")
finally:
    sock.close()
