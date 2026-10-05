
class ContextManager:
    def build(self, message, memories=None):
        memories = memories or []
        return {
            "message": message,
            "memory": memories
        }
