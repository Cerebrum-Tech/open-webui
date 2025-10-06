# STB-AI Authentication Debugging Guide

## Issues Fixed

### 1. **Field Name Mismatch** ✅
The API might return data with different field naming conventions. Now handles:
- `fullName`, `FullName`, `full_name`, `name`, `Name`
- `userName`, `UserName`, `username`, `user_name`, `Username`
- `unitID`, `UnitID`, `unitId`, `unit_id`, `birimID`
- `unitName`, `UnitName`, `unit_name`, `birimAdi`, `birimName`

### 2. **Empty Username Validation** ✅
Now validates that username is not empty before creating user accounts.

### 3. **Comprehensive Logging** ✅
Every step of the authentication process is now logged with detailed information.

## How to Test

### Step 1: Check Server Logs

When the authentication runs, you should see detailed logs like:

```
======================================================================
STB-AI AUTH ENDPOINT CALLED
======================================================================
Client IP: 192.168.1.100
User-Agent: Mozilla/5.0...
All cookies received: ['STB-AI', 'sessionid', ...]

=== validate_stb_ai_user called ===
Request path: /api/v1/auths/stb-ai/auth
Request method: POST
STB-AI Auth Enabled: True
Available cookies: ['STB-AI', ...]

STB-AI cookie found. Value starts with: abc123...

=== STB-AI Authentication Attempt ===
API URL: https://intranet.sanayi.gov.tr/api/userai
Cookie value (first 20 chars): abc123...
Cookie value length: 256
Sending POST request to intranet API...
API Response Status Code: 200
API Response Data: {...}

=== STB-AI Authentication SUCCESSFUL ===
Raw user data keys: ['userName', 'fullName', 'unitID', 'unitName']
Raw user data: {'userName': 'mutlu.kartin', 'fullName': 'Mutlu Kartın', ...}
Extracted Full Name: Mutlu Kartın
Extracted Username: mutlu.kartin
Extracted Unit ID: 123
Extracted Unit Name: Bilgi İşlem Dairesi Başkanlığı

Processing authentication for user:
  Username: mutlu.kartin
  Full Name: Mutlu Kartın
  Email (generated): mutlu.kartin@sanayi.gov.tr
  Unit ID: 123
  Unit Name: Bilgi İşlem Dairesi Başkanlığı

User found in database with ID: abc-123-def
Token created (first 20 chars): eyJhbGciOiJIUzI1NiIs...

======================================================================
STB-AI AUTHENTICATION SUCCESSFUL - Returning session data
User ID: abc-123-def
User Email: mutlu.kartin@sanayi.gov.tr
User Name: Mutlu Kartın
User Role: user
======================================================================
```

### Step 2: Common Issues and Solutions

#### Issue: "STB-AI cookie not found"
**Logs will show:**
```
Available cookies: []
STB-AI cookie not found in request
```

**Solutions:**
1. Make sure you're logged into intranet.sanayi.gov.tr first
2. Check cookie domain - it must be accessible from your Open WebUI domain
3. Enable debug mode in browser to see all cookies
4. Check CORS settings

#### Issue: "Username not found in authentication response"
**Logs will show:**
```
Raw user data keys: ['someField', 'anotherField']
Username is empty or not found in API response!
```

**Solutions:**
1. Check the exact field names in "Raw user data"
2. Add those field names to the field name handling in `stb_ai_auth.py`
3. Contact the API team to confirm field names

#### Issue: "API timeout" or "Connection error"
**Logs will show:**
```
=== STB-AI Authentication TIMEOUT ===
Timeout error: ...
Timeout setting: 10 seconds
```

**Solutions:**
1. Increase timeout: `export STB_AI_API_TIMEOUT=30`
2. Check network connectivity to intranet.sanayi.gov.tr
3. Check firewall rules

#### Issue: API returns `status: false`
**Logs will show:**
```
=== STB-AI Authentication FAILED ===
Status: False
Error message: Kullanıcı oturumu kapalı
Full response data: {...}
```

**Solutions:**
1. User session may have expired - login to intranet again
2. Cookie may be invalid - clear cookies and login again
3. User account may not exist in the system

### Step 3: Testing Checklist

- [ ] Server is running
- [ ] Logged into intranet.sanayi.gov.tr in the same browser
- [ ] STB-AI cookie is present (check browser DevTools > Application > Cookies)
- [ ] Open WebUI authentication page loads
- [ ] Check browser console for any JavaScript errors
- [ ] Check server logs for detailed authentication flow
- [ ] Verify CORS settings if calling from different domain

### Step 4: Manual Testing

You can test the endpoints manually:

```bash
# Test check endpoint
curl -X GET \
  http://your-server:8080/api/v1/auths/stb-ai/check \
  -H "Cookie: STB-AI=your-cookie-value" \
  -v

# Test auth endpoint
curl -X POST \
  http://your-server:8080/api/v1/auths/stb-ai/auth \
  -H "Cookie: STB-AI=your-cookie-value" \
  -v
```

### Step 5: Enable Debug Mode

Add to your environment:
```bash
export STB_AI_DEBUG=true
export STB_AI_AUTH_ENABLED=true
```

## Environment Variables Reference

```bash
# Enable/disable STB-AI authentication (default: true)
STB_AI_AUTH_ENABLED=true

# Intranet API URL
STB_AI_API_URL=https://intranet.sanayi.gov.tr/api/userai

# Cookie name (default: STB-AI)
STB_AI_COOKIE_NAME=STB-AI

# Auto-register new users (default: true)
STB_AI_AUTO_REGISTER=true

# Default role for new users (default: user)
STB_AI_DEFAULT_USER_ROLE=user

# Email domain for auto-generated emails
STB_AI_EMAIL_DOMAIN=sanayi.gov.tr

# API timeout in seconds (default: 10)
STB_AI_API_TIMEOUT=30

# Enable debug logging (default: false)
STB_AI_DEBUG=true

# CORS configuration (if needed)
CORS_ALLOW_ORIGIN=https://yapayzeka.sanayi.gov.tr;https://intranet.sanayi.gov.tr
```

## What the Logs Tell You

| Log Message | Meaning | Action |
|-------------|---------|--------|
| "STB-AI cookie found" | Cookie is present | ✅ Good |
| "STB-AI cookie not found" | No cookie in request | Check browser cookies |
| "API Response Status Code: 200" | API call succeeded | ✅ Good |
| "API Response Status Code: 401/403" | Authentication failed | Check cookie validity |
| "Raw user data keys: [...]" | Shows actual field names | Use to fix field mapping |
| "Username is empty" | API didn't return username | Check field names or API |
| "User found in database" | Existing user login | ✅ Good |
| "User not found - Auto-registering" | New user creation | ✅ Good |
| "AUTHENTICATION SUCCESSFUL" | Login complete | ✅ Good |

## Need More Help?

1. Enable `STB_AI_DEBUG=true`
2. Reproduce the issue
3. Copy the full log output
4. Share logs with the team

The logs now show:
- Every cookie received
- Exact API request/response
- All field names in the response
- Every step of user creation/login
- Token generation
- Permission assignment
