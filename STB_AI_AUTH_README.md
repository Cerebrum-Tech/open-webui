# STB-AI Authentication Integration

This document describes the STB-AI cookie-based authentication integration for Open WebUI with the intranet.sanayi.gov.tr system.

## Overview

The STB-AI authentication system allows users to authenticate using their existing session from intranet.sanayi.gov.tr. When a user has a valid STB-AI cookie, they can automatically authenticate with Open WebUI without needing to enter credentials.

## How It Works

1. **Cookie Detection**: The system checks for the presence of an `STB-AI` cookie in the user's browser.

2. **API Validation**: If the cookie is present, it sends the cookie value to `https://intranet.sanayi.gov.tr/api/userai` with the `idRef` parameter.

3. **Response Handling**:
   - If `status = true`: The API returns user information (name, Windows username, unit ID, unit name)
   - If `status = false`: Authentication fails with an error message

4. **User Creation/Update**: If authentication is successful:
   - For new users: Automatically creates an account
   - For existing users: Updates their information

## Configuration

### Environment Variables

Add these to your `.env` file or environment:

```bash
# Enable/disable STB-AI authentication (default: true)
STB_AI_AUTH_ENABLED=true

# Intranet API URL (default: https://intranet.sanayi.gov.tr/api/userai)
STB_AI_API_URL=https://intranet.sanayi.gov.tr/api/userai

# Cookie name (default: STB-AI)
STB_AI_COOKIE_NAME=STB-AI

# Auto-register new users (default: true)
STB_AI_AUTO_REGISTER=true

# Default role for new users (default: user)
STB_AI_DEFAULT_USER_ROLE=user

# Email domain for auto-generated emails (default: sanayi.gov.tr)
STB_AI_EMAIL_DOMAIN=sanayi.gov.tr

# API timeout in seconds (default: 10)
STB_AI_API_TIMEOUT=10

# Update user info on each login (default: true)
STB_AI_UPDATE_USER_INFO=true

# Enable debug logging (default: false)
STB_AI_DEBUG=false
```

### CORS Configuration

If you encounter CORS issues, add the yapayzeka subdomain to the allowed origins:

```bash
CORS_ALLOW_ORIGIN=https://yapayzeka.sanayi.gov.tr;https://intranet.sanayi.gov.tr;http://localhost:5173
```

## API Endpoints

### 1. Check STB-AI Cookie Status

```
GET /api/v1/auths/stb-ai/check
```

Returns whether a valid STB-AI cookie is present and user information if authenticated.

**Response:**
```json
{
  "authenticated": true,
  "user_info": {
    "full_name": "Mutlu Kartın",
    "username": "mutlu.kartin",
    "unit_name": "Bilgi İşlem Dairesi Başkanlığı"
  }
}
```

### 2. Authenticate with STB-AI

```
POST /api/v1/auths/stb-ai/auth
```

Authenticates the user using their STB-AI cookie and creates a session.

**Response:**
```json
{
  "token": "eyJ...",
  "token_type": "Bearer",
  "expires_at": 1234567890,
  "id": "user-id",
  "email": "mutlu.kartin@sanayi.gov.tr",
  "name": "Mutlu Kartın",
  "role": "user",
  "profile_image_url": "/user.png",
  "permissions": {...}
}
```

## Frontend Integration

The frontend automatically checks for STB-AI authentication when users visit the login page. If a valid STB-AI cookie is detected, the user is automatically logged in without seeing the login form.

## Testing

Use the provided test script to verify the integration:

```bash
python test_stb_ai_auth.py
```

To test with a real STB-AI cookie:
1. Log in to intranet.sanayi.gov.tr
2. Get the STB-AI cookie value from your browser's developer tools
3. Update the test script with the cookie value
4. Run the tests

## Security Considerations

1. **HTTPS Required**: Always use HTTPS in production to protect cookie transmission
2. **Cookie Security**: The STB-AI cookie is validated with the external API on each authentication
3. **Token Expiry**: Session tokens expire after the configured duration
4. **User Verification**: Each authentication request is verified with intranet.sanayi.gov.tr

## Troubleshooting

### CORS Errors
- Ensure the yapayzeka subdomain is whitelisted in CORS_ALLOW_ORIGIN
- Check that the API endpoints are accessible from your domain

### Authentication Failures
- Verify the STB-AI cookie is present and valid
- Check the API logs with `STB_AI_DEBUG=true`
- Ensure the intranet.sanayi.gov.tr API is accessible

### User Creation Issues
- Check that `STB_AI_AUTO_REGISTER` is enabled
- Verify database write permissions
- Review logs for specific error messages

## Support

For issues or questions about the STB-AI authentication integration:
1. Check the logs in `/data/open-webui/backend/logs/`
2. Enable debug mode with `STB_AI_DEBUG=true`
3. Contact the system administrator

## Additional Notes

As mentioned in the original email:
- The "Keşfet" (Discover) button is currently active for specific users
- Manual AI model activation may be needed for certain users
- System logout integration will be addressed in future updates

