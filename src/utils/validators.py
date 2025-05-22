import re
import json
from typing import Union, Dict, Any
from urllib.parse import urlparse

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

def validate_url(url: str) -> bool:
    """
    Validate if the given URL is properly formatted.
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not url:
        return False
        
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    try:
        result = re.match(regex, url) is not None
        if result:
            parsed = urlparse(url)
            return all([parsed.scheme, parsed.netloc])
        return False
    except Exception:
        return False

def validate_json(json_data: Union[str, Dict]) -> bool:
    """
    Validate if the given data is valid JSON.
    
    Args:
        json_data (Union[str, Dict]): JSON string or dictionary to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if isinstance(json_data, dict):
        return True
        
    if not isinstance(json_data, str):
        return False
        
    try:
        json.loads(json_data)
        return True
    except ValueError:
        return False

def validate_method(method: str) -> bool:
    """
    Validate if the given HTTP method is supported.
    
    Args:
        method (str): HTTP method to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    valid_methods = {'GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'}
    return method.upper() in valid_methods

def validate_headers(headers: Dict[str, Any]) -> bool:
    """
    Validate if the given headers are properly formatted.
    
    Args:
        headers (Dict[str, Any]): Headers dictionary to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(headers, dict):
        return False
        
    for key, value in headers.items():
        if not isinstance(key, str) or not isinstance(value, (str, int, float, bool)):
            return False
    return True

def validate_params(params: Dict[str, Any]) -> bool:
    """
    Validate if the given query parameters are properly formatted.
    
    Args:
        params (Dict[str, Any]): Query parameters to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(params, dict):
        return False
        
    return all(isinstance(k, str) for k in params.keys())