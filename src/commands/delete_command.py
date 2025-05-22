from typing import Dict, Any
from ..api_client.http_client import HttpClient

def execute_delete_request(url: str) -> Dict[str, Any]:
    client = HttpClient()
    return client.delete(url)