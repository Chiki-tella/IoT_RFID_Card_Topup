# test_rfid.py
# Simple test for MFRC522 on ESP8266 using your wiring
# Compatible with the mfrc522.py you have (wendlers version)

from mfrc522 import MFRC522
import time

# === Your exact wiring (GPIO numbers) ===
SCK  = 14   # D5  → GPIO14
MOSI = 13   # D7  → GPIO13
MISO = 12   # D6  → GPIO12
RST  = 0    # D3  → GPIO0
CS   = 2    # D4  → GPIO2 (SDA/CS)

print("Starting MFRC522 test...")

# Initialize reader with your pins
reader = MFRC522(SCK, MOSI, MISO, RST, CS)

print("Reader initialized.")
print("Place a MIFARE card near the reader...")
print("Press Ctrl+C in terminal to stop.")

try:
    while True:
        # 1. Look for a card (request)
        (status, uid) = reader.request(reader.REQIDL)
        
        if status == reader.OK:
            print("\nCard detected!")
            
            # 2. Get UID (anti-collision)
            (status, uid) = reader.anticoll()
            
            if status == reader.OK:
                # Format UID nicely (hex uppercase, no spaces)
                uid_str = ''.join('{:02X}'.format(x) for x in uid)
                print("UID:", uid_str)
            else:
                print("Failed to read UID (anticoll error)")
                
        time.sleep(0.3)  # Don't spin CPU too hard

except KeyboardInterrupt:
    print("\nStopped by user.")