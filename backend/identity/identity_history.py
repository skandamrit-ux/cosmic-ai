"""Identity change history."""

class IdentityHistory:
    def __init__(self):
        self.entries = []

    def record(self, old_name, new_name):
        self.entries.append({
            "old_name": old_name,
            "new_name": new_name
        })

    def all(self):
        return list(self.entries)
