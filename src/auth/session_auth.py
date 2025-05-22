import requests

class SessionAuth:
    def __init__(self):
        self.sessions = {}

    def login(self, name, login_url, payload):
        session = requests.Session()
        response = session.post(login_url, data=payload)
        if response.ok:
            self.sessions[name] = session
            return True
        return False

    def get_session(self, name):
        return self.sessions.get(name)

    def list_sessions(self):
        return list(self.sessions.keys())