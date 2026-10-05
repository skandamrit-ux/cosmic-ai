"""Persistent COSMIC identity management."""

DEFAULT_IDENTITY = {
    "name": "COSMIC",
    "version": "0.1.0"
}


class IdentityManager:
    def __init__(self, identity=None):
        self.identity = dict(DEFAULT_IDENTITY)
        if identity:
            self.identity.update(identity)

    def get_name(self):
        return self.identity["name"]

    def rename(self, new_name):
        new_name = str(new_name).strip()
        if not new_name:
            raise ValueError("Identity name cannot be empty")
        self.identity["name"] = new_name
        return new_name
