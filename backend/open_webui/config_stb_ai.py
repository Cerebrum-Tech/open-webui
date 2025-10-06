"""
STB-AI Authentication Configuration
This file contains configuration settings for the STB-AI authentication integration
"""

import os
from typing import Optional

# STB-AI Authentication Settings
STB_AI_AUTH_ENABLED = os.getenv("STB_AI_AUTH_ENABLED", "true").lower() == "true"

# Intranet API URL (can be overridden via environment variable)
STB_AI_API_URL = os.getenv("STB_AI_API_URL", "https://intranet.sanayi.gov.tr/api/userai")

# Cookie name for STB-AI authentication
STB_AI_COOKIE_NAME = os.getenv("STB_AI_COOKIE_NAME", "STB-AI")

# Auto-registration settings
STB_AI_AUTO_REGISTER = os.getenv("STB_AI_AUTO_REGISTER", "true").lower() == "true"
STB_AI_DEFAULT_USER_ROLE = os.getenv("STB_AI_DEFAULT_USER_ROLE", "user")

# Domain for auto-generated emails
STB_AI_EMAIL_DOMAIN = os.getenv("STB_AI_EMAIL_DOMAIN", "sanayi.gov.tr")

# CORS settings for yapayzeka subdomain
# If you need to allow the yapayzeka subdomain, add it to CORS_ALLOW_ORIGIN
# Example: CORS_ALLOW_ORIGIN=https://yapayzeka.sanayi.gov.tr;https://intranet.sanayi.gov.tr

# Timeout for external API calls (in seconds)
STB_AI_API_TIMEOUT = int(os.getenv("STB_AI_API_TIMEOUT", "10"))

# Whether to update user info on each login
STB_AI_UPDATE_USER_INFO = os.getenv("STB_AI_UPDATE_USER_INFO", "true").lower() == "true"

# Debug mode for STB-AI authentication
STB_AI_DEBUG = os.getenv("STB_AI_DEBUG", "false").lower() == "true"

def get_stb_ai_config():
    """Get STB-AI authentication configuration"""
    return {
        "enabled": STB_AI_AUTH_ENABLED,
        "api_url": STB_AI_API_URL,
        "cookie_name": STB_AI_COOKIE_NAME,
        "auto_register": STB_AI_AUTO_REGISTER,
        "default_role": STB_AI_DEFAULT_USER_ROLE,
        "email_domain": STB_AI_EMAIL_DOMAIN,
        "api_timeout": STB_AI_API_TIMEOUT,
        "update_user_info": STB_AI_UPDATE_USER_INFO,
        "debug": STB_AI_DEBUG
    }

