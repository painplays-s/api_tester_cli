import requests
import time

class OAuth2Auth:
    def __init__(self):
        self.tokens = {}

    def add_oauth2_flow(self, name, token_url, client_id, client_secret, scope):
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": scope,
        }
        response = requests.post(token_url, data=data)
        if response.ok:
            token_data = response.json()
            token_data["expires_at"] = time.time() + token_data.get("expires_in", 3600)
            self.tokens[name] = token_data
            return token_data["access_token"]
        else:
            raise Exception("OAuth2 token request failed")

    def get_token(self, name):
        token_data = self.tokens.get(name)
        if not token_data:
            return ""
        if time.time() > token_data.get("expires_at", 0):
            return ""
        return token_data.get("access_token", "")

    def list_tokens(self):
        return list(self.tokens.keys())