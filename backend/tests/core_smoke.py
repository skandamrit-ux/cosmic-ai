
import requests

BASE = "http://127.0.0.1:8000"

checks = [
    "/api/health",
    "/api/status",
    "/api/routes",
    "/api/memory/count",
    "/api/providers",
    "/api/ai/gemini",
    "/api/runtime",
    "/api/system/full"
]

for path in checks:
    r = requests.get(BASE + path, timeout=10)
    print(path, r.status_code, r.text[:300])

print("COSMIC CORE SMOKE TEST COMPLETE")
