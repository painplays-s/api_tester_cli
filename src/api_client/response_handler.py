import json
from requests import Response
from typing import Dict, Any

class ResponseHandler:
    def handle_response(self, response: Response) -> Dict[str, Any]:
        result = {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'elapsed_time': response.elapsed.total_seconds(),
        }

        try:
            result['body'] = response.json()
        except json.JSONDecodeError:
            result['body'] = response.text

        return result