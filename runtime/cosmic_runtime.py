import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "runtime" / "logs" / "server.log"
PID = ROOT / "runtime" / "state" / "server.pid"

process = None

def shutdown(*_):
    global process
    if process and process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
    PID.unlink(missing_ok=True)
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

LOG.parent.mkdir(parents=True, exist_ok=True)
PID.parent.mkdir(parents=True, exist_ok=True)

with LOG.open("a", buffering=1) as log:
    log.write("\n[COSMIC Runtime] Starting backend...\n")

    process = subprocess.Popen(
        [sys.executable, "-m", "backend.app"],
        cwd=str(ROOT),
        stdout=log,
        stderr=subprocess.STDOUT,
    )

    PID.write_text(str(process.pid))
    log.write(f"[COSMIC Runtime] Backend PID: {process.pid}\n")

    while process.poll() is None:
        time.sleep(2)

    log.write(
        f"[COSMIC Runtime] Backend stopped with code {process.returncode}\n"
    )
