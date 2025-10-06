#!/usr/bin/env python3
"""
Test script for STB-AI Authentication
This script tests the STB-AI authentication flow with the intranet.sanayi.gov.tr API
"""

import requests
import json
import sys
from urllib.parse import urljoin

# Configuration
BASE_URL = "http://localhost:8080"  # Change this to your Open WebUI URL
API_BASE_URL = f"{BASE_URL}/api/v1"

def test_stb_ai_check():
    """Test the STB-AI check endpoint"""
    print("Testing STB-AI check endpoint...")
    
    # Test without cookie
    response = requests.get(f"{API_BASE_URL}/auths/stb-ai/check")
    print(f"Response without cookie: {response.json()}")
    
    # You can test with a cookie by adding it to the request
    # cookies = {"STB-AI": "your-test-cookie-value"}
    # response = requests.get(f"{API_BASE_URL}/auths/stb-ai/check", cookies=cookies)
    # print(f"Response with cookie: {response.json()}")

def test_stb_ai_auth():
    """Test the STB-AI authentication endpoint"""
    print("\nTesting STB-AI authentication endpoint...")
    
    # To test this, you need a valid STB-AI cookie
    # Uncomment and modify the following lines to test with a real cookie
    
    # cookies = {"STB-AI": "your-valid-stb-ai-cookie-value"}
    # response = requests.post(f"{API_BASE_URL}/auths/stb-ai/auth", cookies=cookies)
    # 
    # if response.status_code == 200:
    #     print("Authentication successful!")
    #     user_data = response.json()
    #     print(f"User: {user_data.get('name')} ({user_data.get('email')})")
    #     print(f"Token: {user_data.get('token')[:20]}...")
    # else:
    #     print(f"Authentication failed: {response.status_code}")
    #     print(response.json())
    
    print("Note: To fully test authentication, you need a valid STB-AI cookie from intranet.sanayi.gov.tr")

def test_manual_api_call():
    """Test direct API call to intranet.sanayi.gov.tr"""
    print("\nTesting direct API call to intranet.sanayi.gov.tr...")
    
    # This is for testing the external API directly
    # You need a valid STB-AI cookie value for this to work
    
    api_url = "https://intranet.sanayi.gov.tr/api/userai"
    
    # Replace with actual cookie value
    cookie_value = "your-stb-ai-cookie-value"
    
    if cookie_value == "your-stb-ai-cookie-value":
        print("Please replace 'your-stb-ai-cookie-value' with an actual STB-AI cookie value to test")
        return
    
    try:
        response = requests.post(
            api_url,
            json={"idRef": cookie_value},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.json().get("status") is True:
            data = response.json().get("data", {})
            print(f"\nUser Information:")
            print(f"  Full Name: {data.get('fullName')}")
            print(f"  Username: {data.get('userName')}")
            print(f"  Unit ID: {data.get('unitID')}")
            print(f"  Unit Name: {data.get('unitName')}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Main test function"""
    print("=" * 60)
    print("STB-AI Authentication Test Suite")
    print("=" * 60)
    
    # Test endpoints
    test_stb_ai_check()
    test_stb_ai_auth()
    
    # Optional: Test direct API call
    # test_manual_api_call()
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)
    
    print("\nInstructions for full testing:")
    print("1. Obtain a valid STB-AI cookie from intranet.sanayi.gov.tr")
    print("2. Update the cookie value in this script")
    print("3. Run the tests again with the valid cookie")
    print("4. Verify that authentication works correctly")

if __name__ == "__main__":
    main()

