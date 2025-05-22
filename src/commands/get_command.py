from typing import Dict, Any, Optional
from ..api_client.http_client import HttpClient

def execute_get_request(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    client = HttpClient()
    return client.get(url, params)