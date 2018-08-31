class Rule:
    def __init__(self, r):
        self.description = r['description']
        self.type = r['issueType']
        self.category = r['category']['name']
        try:
            self.url = r['urls'][0]['value']
        except KeyError:
            self.url = ""
