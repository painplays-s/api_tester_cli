import os
import json
from typing import Dict, Any
from src.api_client.http_client import HttpClient
from src.utils.config import Config
from src.utils.validators import validate_url, validate_json

class Menu:
    def __init__(self):
        self.client = HttpClient()
        self.config = Config()
        self.history = []

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
    7. Exit
    """)

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
            response = self.client.get(url, params=params_dict)
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
            response = self.client.post(url, data=data_dict)
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
        print(json.dumps(response['body'], indent=2))
        input("\nPress Enter to continue...")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-7): ")
            
            if choice == '1':
                self.handle_get_request()
            elif choice == '2':
                self.handle_post_request()
            elif choice == '3':
                url = input("Enter URL: ")
                data = input("Enter request body (JSON format): ")
                if validate_url(url) and validate_json(data):
                    response = self.client.put(url, data=json.loads(data))
                    self.history.append({"method": "PUT", "url": url, "response": response})
                    self.display_response(response)
            elif choice == '4':
                url = input("Enter URL: ")
                if validate_url(url):
                    response = self.client.delete(url)
                    self.history.append({"method": "DELETE", "url": url, "response": response})
                    self.display_response(response)
            elif choice == '5':
                self.configure_headers()
            elif choice == '6':
                self.view_history()
            elif choice == '7':
                print("Thank you for using API Tester CLI!")
                break
            else:
                input("Invalid choice. Press Enter to continue...")

def main():
    menu = Menu()
    menu.run()

if __name__ == "__main__":
    main()