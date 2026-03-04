import socket
import sys
import time
import random
import string
from datetime import datetime

DEFAULT_PORT = 12345
PAYLOAD_SIZE = 200   # bytes per packet

def generate_random_payload(size=200):
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=size)).encode()

if __name__ == "__main__":
    # Get port from argument or use default
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', port))
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] UDP Server started")
    print(f"Listening on port {port}")
    print("Waiting for client to initiate connection...\n")
    
    client_addr = None
    packets_sent = 0
    packets_received = 0
    start_time = time.time()
    
    try:
        while True:
            # Receive data (with 1-second timeout)
            try:
                sock.settimeout(1.0)
                data, addr = sock.recvfrom(4096)
                
                if client_addr is None:
                    client_addr = addr
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Client connected: {addr[0]}:{addr[1]}\n")
                
                packets_received += 1
                
            except socket.timeout:
                pass
            
            # Send random payload back (once we know the client)
            if client_addr:
                payload = generate_random_payload(PAYLOAD_SIZE)
                sock.sendto(payload, client_addr)
                packets_sent += 1
            
            # Show live stats every 5 seconds
            elapsed = time.time() - start_time
            if int(elapsed) % 5 == 0 and int(elapsed) > 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ↑ Sent: {packets_sent} | ↓ Received: {packets_received} | "
                      f"Rate: {packets_sent/elapsed:.1f} pkt/s", end="\r")
            
            time.sleep(0.05)  # prevent 100% CPU
            
    except KeyboardInterrupt:
        print("\n\nServer stopped by user (Ctrl+C)")
    finally:
        sock.close()
