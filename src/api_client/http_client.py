import requests
from typing import Dict, Any, Optional
from .response_handler import ResponseHandler

class HttpClient:
    def __init__(self):
        self.headers: Dict[str, str] = {}
        self.response_handler = ResponseHandler()

    def set_headers(self, headers: Dict[str, str]):
        self.headers.update(headers)

    def get(self, url: str, params: Optional[Dict[str, Any]] = None, session: Optional[requests.Session] = None) -> Dict[str, Any]:
        req = session if session else requests
        response = req.get(url, headers=self.headers, params=params)
        return self.response_handler.handle_response(response)

    def post(self, url: str, data: Optional[Dict[str, Any]] = None, session: Optional[requests.Session] = None) -> Dict[str, Any]:
        req = session if session else requests
        response = req.post(url, headers=self.headers, json=data)
        return self.response_handler.handle_response(response)

    def put(self, url: str, data: Optional[Dict[str, Any]] = None, session: Optional[requests.Session] = None) -> Dict[str, Any]:
        req = session if session else requests
        response = req.put(url, headers=self.headers, json=data)
        return self.response_handler.handle_response(response)

    def delete(self, url: str, session: Optional[requests.Session] = None) -> Dict[str, Any]:
        req = session if session else requests
        response = req.delete(url, headers=self.headers)
        return self.response_handler.handle_response(response)