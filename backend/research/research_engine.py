
class ResearchEngine:
    def plan(self, query):
        return {
            "success": True,
            "query": query,
            "steps": [
                "understand",
                "retrieve",
                "compare",
                "verify",
                "summarize"
            ]
        }
