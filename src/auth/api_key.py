class APIKeyAuth:
    def __init__(self):
        self.api_keys = {}

    def add_api_key(self, name, key):
        self.api_keys[name] = key

    def get_api_key(self, name):
        return self.api_keys.get(name)

    def list_api_keys(self):
        return list(self.api_keys.keys())