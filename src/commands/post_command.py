from typing import Dict, Any, Optional
from ..api_client.http_client import HttpClient

def execute_post_request(url: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    client = HttpClient()
    return client.post(url, data)