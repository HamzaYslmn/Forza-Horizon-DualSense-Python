"""Quick smoke-test: sends known effects to DSX and prints the JSON payloads.
Run from src/: uv run test_dsx.py

DSX must be running and listening on 127.0.0.1:6969.
"""
import json
import socket
import time
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from modules.dualsense.triggers import off, rigid, vibration, feedback, vibration_wall, build_wall
from modules.dsx.main import build_packet_bytes, autodetect_port, is_dsx_running

HOST = "127.0.0.1"
PORT = 6969
CTRL = 0
DELAY = 0.8  # seconds between effects

def send(sock, left, right, label: str):
    data = build_packet_bytes(CTRL, left, right)
    sock.sendto(data, (HOST, PORT))
    parsed = json.loads(data)
    print(f"\n[{label}]")
    for inst in parsed["instructions"]:
        trig = "L2" if inst["parameters"][1] == 1 else "R2"
        print(f"  {trig}: {inst['parameters'][2:]}")

def main():
    print(f"DSX running: {is_dsx_running()}")
    detected = autodetect_port()
    print(f"Detected port: {detected}  (using {PORT})")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    effects = [
        (off(),            off(),                         "both OFF"),
        (rigid(80),        rigid(8),                      "L2 brake firm / R2 light ramp"),
        (vibration(10,20), vibration(20,10),              "L2 ABS pulse / R2 rev buzz"),
        (build_wall(2),    vibration_wall(3, 100, 2),     "L2 end-wall / R2 vibration_wall"),
        (feedback([0]*8 + [8,8]), off(),                  "L2 MULTI_FEEDBACK wall / R2 off"),
        (off(),            off(),                         "reset - both OFF"),
    ]

    for left, right, label in effects:
        send(sock, left, right, label)
        time.sleep(DELAY)

    sock.close()
    print("\nDone.")

if __name__ == "__main__":
    main()
