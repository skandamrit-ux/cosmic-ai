
import time
import platform
import os

START_TIME = time.time()

def info():
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "pid": os.getpid(),
        "uptime": round(time.time() - START_TIME, 2)
    }
