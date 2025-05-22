import os
import json
from typing import Dict, Any
from src.api_client.http_client import HttpClient
from src.utils.config import Config
from src.utils.validators import validate_url, validate_json

from src.auth.api_key import APIKeyAuth
from src.auth.basic_auth import BasicAuth
from src.auth.bearer_token import BearerTokenAuth
from src.auth.oauth2 import OAuth2Auth
from src.auth.session_auth import SessionAuth

class Menu:
    def __init__(self):
        self.client = HttpClient()
        self.config = Config()
        self.history = []

        # Auth managers
        self.api_key_auth = APIKeyAuth()
        self.basic_auth = BasicAuth()
        self.bearer_auth = BearerTokenAuth()
        self.oauth2_auth = OAuth2Auth()
        self.session_auth = SessionAuth()

        # Current auth context
        self.current_auth_type = None
        self.current_auth_name = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        self.clear_screen()
        print("""
    === API Tester CLI ===
    1. GET Request
    2. POST Request
    3. PUT Request
    4. DELETE Request
    5. Configure Headers
    6. View History
    7. Authorization Management
    8. Exit
    """)
        if self.current_auth_type and self.current_auth_name:
            print(f"Active Auth: {self.current_auth_type} ({self.current_auth_name})")

    def handle_get_request(self):
        url = input("Enter URL: ")
        if not validate_url(url):
            input("Invalid URL. Press Enter to continue...")
            return

        params = input("Enter query parameters (JSON format) or press Enter to skip: ")
        if params and not validate_json(params):
            input("Invalid JSON format. Press Enter to continue...")
            return

        try:
            params_dict = json.loads(params) if params else None
            headers = self.get_auth_headers()
            response = self.client.get(url, params=params_dict, headers=headers)
            self.history.append({"method": "GET", "url": url, "response": response})
            self.display_response(response)
        except Exception as e:
            input(f"Error: {str(e)}. Press Enter to continue...")

    def handle_post_request(self):
        url = input("Enter URL: ")
        if not validate_url(url):
            input("Invalid URL. Press Enter to continue...")
            return

        data = input("Enter request body (JSON format): ")
        if not validate_json(data):
            input("Invalid JSON format. Press Enter to continue...")
            return

        try:
            data_dict = json.loads(data)
            headers = self.get_auth_headers()
            response = self.client.post(url, data=data_dict, headers=headers)
            self.history.append({"method": "POST", "url": url, "response": response})
            self.display_response(response)
        except Exception as e:
            input(f"Error: {str(e)}. Press Enter to continue...")

    def configure_headers(self):
        print("\nCurrent headers:", json.dumps(self.client.headers, indent=2))
        new_headers = input("Enter new headers (JSON format) or press Enter to skip: ")
        if new_headers:
            try:
                headers_dict = json.loads(new_headers)
                self.client.set_headers(headers_dict)
                print("Headers updated successfully!")
            except json.JSONDecodeError:
                print("Invalid JSON format")
        input("Press Enter to continue...")

    def view_history(self):
        if not self.history:
            input("No history available. Press Enter to continue...")
            return

        print("\n=== Request History ===")
        for i, entry in enumerate(self.history[-10:], 1):
            print(f"\n{i}. {entry['method']} {entry['url']}")
            print(f"Status: {entry['response']['status_code']}")
        input("\nPress Enter to continue...")

    def display_response(self, response: Dict[str, Any]):
        print("\n=== Response ===")
        print(f"Status Code: {response['status_code']}")
        print(f"Time: {response['elapsed_time']}s")
        print("\nHeaders:")
        print(json.dumps(response['headers'], indent=2))
        print("\nBody:")
        try:
            print(json.dumps(response['body'], indent=2))
        except Exception:
            print(str(response['body']))
        input("\nPress Enter to continue...")

    def get_auth_headers(self):
        """Return headers for the currently selected auth method."""
        if self.current_auth_type == "API Key":
            key = self.api_key_auth.get_api_key(self.current_auth_name)
            if key:
                return {"x-api-key": key}
        elif self.current_auth_type == "Basic Auth":
            return self.basic_auth.get_header(self.current_auth_name)
        elif self.current_auth_type == "Bearer Token":
            return self.bearer_auth.get_header(self.current_auth_name)
        elif self.current_auth_type == "OAuth2":
            token = self.oauth2_auth.get_token(self.current_auth_name)
            if token:
                return {"Authorization": f"Bearer {token}"}
        # Session Auth handled at request level, not via headers
        return {}

    def show_auth_menu(self):
        while True:
            self.clear_screen()
            print("\nAuthorization Management:")
            print("1. Manage API Keys")
            print("2. Manage Basic Auth")
            print("3. Manage Bearer Tokens")
            print("4. Manage OAuth2")
            print("5. Manage Session Auth")
            print("6. Set Active Auth")
            print("0. Back to Main Menu")
            choice = input("Select an option: ")
            if choice == "1":
                self.manage_api_keys()
            elif choice == "2":
                self.manage_basic_auth()
            elif choice == "3":
                self.manage_bearer_tokens()
            elif choice == "4":
                self.manage_oauth2()
            elif choice == "5":
                self.manage_session_auth()
            elif choice == "6":
                self.set_active_auth()
            elif choice == "0":
                break
            else:
                input("Invalid choice. Press Enter to continue...")

    def manage_api_keys(self):
        while True:
            self.clear_screen()
            print("API Key Management")
            print("1. Add API Key")
            print("2. List API Keys")
            print("0. Back")
            choice = input("Select an option: ")
            if choice == "1":
                name = input("Enter key name: ")
                key = input("Enter API key: ")
                self.api_key_auth.add_api_key(name, key)
                print("API key added.")
                input("Press Enter to continue...")
            elif choice == "2":
                print("API Keys:", self.api_key_auth.list_api_keys())
                input("Press Enter to continue...")
            elif choice == "0":
                break

    def manage_basic_auth(self):
        while True:
            self.clear_screen()
            print("Basic Auth Management")
            print("1. Add Credentials")
            print("2. List Credentials")
            print("0. Back")
            choice = input("Select an option: ")
            if choice == "1":
                name = input("Enter credential name: ")
                username = input("Enter username: ")
                password = input("Enter password: ")
                self.basic_auth.add_credentials(name, username, password)
                print("Credentials added.")
                input("Press Enter to continue...")
            elif choice == "2":
                print("Credentials:", self.basic_auth.list_credentials())
                input("Press Enter to continue...")
            elif choice == "0":
                break

    def manage_bearer_tokens(self):
        while True:
            self.clear_screen()
            print("Bearer Token Management")
            print("1. Add Token")
            print("2. List Tokens")
            print("0. Back")
            choice = input("Select an option: ")
            if choice == "1":
                name = input("Enter token name: ")
                token = input("Enter bearer token: ")
                self.bearer_auth.add_token(name, token)
                print("Token added.")
                input("Press Enter to continue...")
            elif choice == "2":
                print("Tokens:", self.bearer_auth.list_tokens())
                input("Press Enter to continue...")
            elif choice == "0":
                break

    def manage_oauth2(self):
        while True:
            self.clear_screen()
            print("OAuth2 Management")
            print("1. Add OAuth2 Token (Client Credentials)")
            print("2. List OAuth2 Tokens")
            print("0. Back")
            choice = input("Select an option: ")
            if choice == "1":
                name = input("Enter token name: ")
                token_url = input("Enter token URL: ")
                client_id = input("Enter client ID: ")
                client_secret = input("Enter client secret: ")
                scope = input("Enter scope (space-separated): ")
                try:
                    token = self.oauth2_auth.add_oauth2_flow(name, token_url, client_id, client_secret, scope)
                    print("OAuth2 token obtained and saved.")
                except Exception as e:
                    print(f"Error: {e}")
                input("Press Enter to continue...")
            elif choice == "2":
                print("OAuth2 Tokens:", self.oauth2_auth.list_tokens())
                input("Press Enter to continue...")
            elif choice == "0":
                break

    def manage_session_auth(self):
        while True:
            self.clear_screen()
            print("Session Auth Management")
            print("1. Login and Save Session")
            print("2. List Sessions")
            print("0. Back")
            choice = input("Select an option: ")
            if choice == "1":
                name = input("Enter session name: ")
                login_url = input("Enter login URL: ")
                payload = input("Enter login payload (JSON): ")
                if not validate_json(payload):
                    print("Invalid JSON.")
                    input("Press Enter to continue...")
                    continue
                payload_dict = json.loads(payload)
                success = self.session_auth.login(name, login_url, payload_dict)
                if success:
                    print("Session saved.")
                else:
                    print("Login failed.")
                input("Press Enter to continue...")
            elif choice == "2":
                print("Sessions:", self.session_auth.list_sessions())
                input("Press Enter to continue...")
            elif choice == "0":
                break

    def set_active_auth(self):
        self.clear_screen()
        print("Set Active Auth")
        print("1. API Key")
        print("2. Basic Auth")
        print("3. Bearer Token")
        print("4. OAuth2")
        print("0. None")
        choice = input("Select auth type: ")
        if choice == "1":
            keys = self.api_key_auth.list_api_keys()
            print("Available API Keys:", keys)
            name = input("Enter key name: ")
            if name in keys:
                self.current_auth_type = "API Key"
                self.current_auth_name = name
                print(f"Active auth set to API Key ({name})")
            else:
                print("Invalid key name.")
        elif choice == "2":
            creds = self.basic_auth.list_credentials()
            print("Available Credentials:", creds)
            name = input("Enter credential name: ")
            if name in creds:
                self.current_auth_type = "Basic Auth"
                self.current_auth_name = name
                print(f"Active auth set to Basic Auth ({name})")
            else:
                print("Invalid credential name.")
        elif choice == "3":
            tokens = self.bearer_auth.list_tokens()
            print("Available Tokens:", tokens)
            name = input("Enter token name: ")
            if name in tokens:
                self.current_auth_type = "Bearer Token"
                self.current_auth_name = name
                print(f"Active auth set to Bearer Token ({name})")
            else:
                print("Invalid token name.")
        elif choice == "4":
            tokens = self.oauth2_auth.list_tokens()
            print("Available OAuth2 Tokens:", tokens)
            name = input("Enter token name: ")
            if name in tokens:
                self.current_auth_type = "OAuth2"
                self.current_auth_name = name
                print(f"Active auth set to OAuth2 ({name})")
            else:
                print("Invalid token name.")
        elif choice == "0":
            self.current_auth_type = None
            self.current_auth_name = None
            print("No active auth.")
        input("Press Enter to continue...")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-8): ")
            if choice == '1':
                self.handle_get_request()
            elif choice == '2':
                self.handle_post_request()
            elif choice == '3':
                url = input("Enter URL: ")
                data = input("Enter request body (JSON format): ")
                if validate_url(url) and validate_json(data):
                    headers = self.get_auth_headers()
                    response = self.client.put(url, data=json.loads(data), headers=headers)
                    self.history.append({"method": "PUT", "url": url, "response": response})
                    self.display_response(response)
            elif choice == '4':
                url = input("Enter URL: ")
                if validate_url(url):
                    headers = self.get_auth_headers()
                    response = self.client.delete(url, headers=headers)
                    self.history.append({"method": "DELETE", "url": url, "response": response})
                    self.display_response(response)
            elif choice == '5':
                self.configure_headers()
            elif choice == '6':
                self.view_history()
            elif choice == '7':
                self.show_auth_menu()
            elif choice == '8':
                print("Thank you for using API Tester CLI!")
                break
            else:
                input("Invalid choice. Press Enter to continue...")

def main():
    menu = Menu()
    menu.run()

if __name__ == "__main__":
    main()