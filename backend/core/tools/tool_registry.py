
class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, function):
        self.tools[name] = function

    def list(self):
        return sorted(self.tools.keys())

    def execute(self, name, **kwargs):
        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")
        return self.tools[name](**kwargs)
