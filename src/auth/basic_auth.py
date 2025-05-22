import base64

class BasicAuth:
    def __init__(self):
        self.credentials = {}

    def add_credentials(self, name, username, password):
        self.credentials[name] = (username, password)

    def get_header(self, name):
        username, password = self.credentials.get(name, ("", ""))
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        return {"Authorization": f"Basic {token}"}

    def list_credentials(self):
        return list(self.credentials.keys())