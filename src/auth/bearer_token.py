class BearerTokenAuth:
    def __init__(self):
        self.tokens = {}

    def add_token(self, name, token):
        self.tokens[name] = token

    def get_header(self, name):
        token = self.tokens.get(name, "")
        return {"Authorization": f"Bearer {token}"}

    def list_tokens(self):
        return list(self.tokens.keys())