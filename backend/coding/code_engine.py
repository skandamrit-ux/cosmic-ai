
class CodeEngine:
    def analyze(self, code):
        return {
            "success": True,
            "language": "unknown",
            "lines": len(code.splitlines()),
            "characters": len(code)
        }
