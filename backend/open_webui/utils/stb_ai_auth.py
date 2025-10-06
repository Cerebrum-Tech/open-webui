"""
STB-AI Authentication Module
Handles authentication via STB-AI cookie and intranet.sanayi.gov.tr API
"""

import logging
import requests
from typing import Optional, Dict, Any
from fastapi import HTTPException, Request, status

from open_webui.env import SRC_LOG_LEVELS
from open_webui.config_stb_ai import (
    STB_AI_API_URL,
    STB_AI_COOKIE_NAME,
    STB_AI_API_TIMEOUT,
    STB_AI_DEBUG,
    STB_AI_AUTH_ENABLED
)

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MAIN"])


class STBAIAuthService:
    """Service for handling STB-AI cookie authentication"""
    
    @staticmethod
    def get_stb_ai_cookie(request: Request) -> Optional[str]:
        """Extract STB-AI cookie from request"""
        cookie_value = request.cookies.get(STB_AI_COOKIE_NAME)
        if cookie_value:
            log.info(f"STB-AI cookie found. Value starts with: {cookie_value[:20]}...")
        else:
            log.info("STB-AI cookie not found in request")
        return cookie_value
    
    @staticmethod
    def authenticate_with_intranet(cookie_value: str) -> Dict[str, Any]:
        """
        Authenticate user with intranet API using STB-AI cookie value
        
        Args:
            cookie_value: The STB-AI cookie value
            
        Returns:
            Dict containing user information if successful
            
        Raises:
            HTTPException if authentication fails
        """
        log.info(f"=== STB-AI Authentication Attempt ===")
        log.info(f"API URL: {STB_AI_API_URL}")
        log.info(f"Cookie value (first 20 chars): {cookie_value[:20]}...")
        log.info(f"Cookie value length: {len(cookie_value)}")
        
        try:
            # Send request to intranet API with idRef parameter
            log.info(f"Sending POST request to intranet API...")
            response = requests.post(
                STB_AI_API_URL,
                json={"idRef": cookie_value},
                headers={
                    "Content-Type": "application/json"
                },
                timeout=STB_AI_API_TIMEOUT
            )
            
            log.info(f"API Response Status Code: {response.status_code}")
            log.info(f"API Response Headers: {dict(response.headers)}")
            
            response.raise_for_status()
            data = response.json()
            
            log.info(f"API Response Data: {data}")
            
            # Check if authentication was successful
            if data.get("status") is True:
                # Extract user data
                user_data = data.get("data", {})
                
                log.info(f"=== STB-AI Authentication SUCCESSFUL ===")
                log.info(f"Raw user data keys: {list(user_data.keys())}")
                log.info(f"Raw user data: {user_data}")
                
                # Handle multiple possible field name formats
                # The API might return camelCase, PascalCase, or other formats
                full_name = (
                    user_data.get("fullName") or 
                    user_data.get("FullName") or 
                    user_data.get("full_name") or
                    user_data.get("name") or
                    user_data.get("Name") or
                    ""
                )
                
                username = (
                    user_data.get("userName") or
                    user_data.get("UserName") or
                    user_data.get("username") or
                    user_data.get("user_name") or
                    user_data.get("Username") or
                    ""
                )
                
                unit_id = (
                    user_data.get("unitID") or
                    user_data.get("UnitID") or
                    user_data.get("unitId") or
                    user_data.get("unit_id") or
                    user_data.get("birimID") or
                    ""
                )
                
                unit_name = (
                    user_data.get("unitName") or
                    user_data.get("UnitName") or
                    user_data.get("unit_name") or
                    user_data.get("birimAdi") or
                    user_data.get("birimName") or
                    ""
                )
                
                log.info(f"Extracted Full Name: {full_name}")
                log.info(f"Extracted Username: {username}")
                log.info(f"Extracted Unit ID: {unit_id}")
                log.info(f"Extracted Unit Name: {unit_name}")
                
                # Validate that we have at least username
                if not username:
                    log.error("Username is empty or not found in API response!")
                    log.error(f"Available fields: {list(user_data.keys())}")
                    return {
                        "status": False,
                        "message": "Username not found in authentication response"
                    }
                
                return {
                    "status": True,
                    "full_name": full_name or username,  # Use username as fallback
                    "username": username,  # Windows username (unique)
                    "unit_id": unit_id,
                    "unit_name": unit_name,
                    "raw_data": user_data  # Keep raw data for reference
                }
            else:
                # Authentication failed
                error_message = data.get("message", "Authentication failed")
                log.warning(f"=== STB-AI Authentication FAILED ===")
                log.warning(f"Status: {data.get('status')}")
                log.warning(f"Error message: {error_message}")
                log.warning(f"Full response data: {data}")
                return {
                    "status": False,
                    "message": error_message
                }
                
        except requests.exceptions.Timeout as e:
            log.error(f"=== STB-AI Authentication TIMEOUT ===")
            log.error(f"Timeout error: {str(e)}")
            log.error(f"Timeout setting: {STB_AI_API_TIMEOUT} seconds")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service timeout"
            )
        except requests.exceptions.RequestException as e:
            log.error(f"=== STB-AI Authentication REQUEST ERROR ===")
            log.error(f"Request error type: {type(e).__name__}")
            log.error(f"Request error details: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                log.error(f"Response status code: {e.response.status_code}")
                log.error(f"Response text: {e.response.text}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to connect to authentication service"
            )
        except Exception as e:
            log.error(f"=== STB-AI Authentication UNEXPECTED ERROR ===")
            log.error(f"Error type: {type(e).__name__}")
            log.error(f"Error details: {str(e)}")
            import traceback
            log.error(f"Stack trace:\n{traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Authentication service error"
            )
    
    @staticmethod
    def validate_stb_ai_user(request: Request) -> Optional[Dict[str, Any]]:
        """
        Validate user using STB-AI cookie
        
        Args:
            request: The FastAPI request object
            
        Returns:
            User data if authentication successful, None otherwise
        """
        log.info(f"=== validate_stb_ai_user called ===")
        log.info(f"Request path: {request.url.path}")
        log.info(f"Request method: {request.method}")
        log.info(f"STB-AI Auth Enabled: {STB_AI_AUTH_ENABLED}")
        log.info(f"Available cookies: {list(request.cookies.keys())}")
        
        if not STB_AI_AUTH_ENABLED:
            log.info("STB-AI authentication is disabled")
            return None
            
        cookie_value = STBAIAuthService.get_stb_ai_cookie(request)
        
        if not cookie_value:
            log.info("No STB-AI cookie found, returning None")
            return None
        
        log.info("STB-AI cookie found, calling authenticate_with_intranet...")
        auth_result = STBAIAuthService.authenticate_with_intranet(cookie_value)
        
        if auth_result.get("status") is True:
            log.info(f"Validation successful for user: {auth_result.get('username')}")
            return auth_result
        else:
            log.warning(f"Validation failed: {auth_result.get('message', 'Unknown error')}")
        
        return None


# Initialize service instance
stb_ai_auth_service = STBAIAuthService()
