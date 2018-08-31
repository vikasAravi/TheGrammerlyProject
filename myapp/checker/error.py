from .rule import Rule

class Error:
    def __init__(self, m):
        self.message = m['message']
        self.title = m['shortMessage']
        self.offset = m['offset']
        self.length = m['length']
        self.suggestions = [suggestion["value"] for suggestion in m['replacements']]
        self.rule = Rule(m['rule'])
    
    def errorType(self):
        if "spelling" in self.title.lower():
            return "spelling"
        else:
            return "grammar"

    def reprJSON(self):
        return dict(message=self.message, type=self.errorType(), title=self.title, offset=self.offset,
        length = self.length, suggestions = self.suggestions, rule = self.rule.__dict__)