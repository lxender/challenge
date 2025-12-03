import subprocess
import signal
import sys

servers = [
    ("frontend", "main.py"),
    ("auth-service", "main.py")
]

processes = []

def cleanup(signum, frame):
    print("\nStopping servers...")
    for p in processes:
        p.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

for directory, script in servers:
    print(f"Starting {directory}/{script}...")
    p = subprocess.Popen(
        [sys.executable, script],
        cwd=directory
    )
    processes.append(p)

for p in processes:
    p.wait()
