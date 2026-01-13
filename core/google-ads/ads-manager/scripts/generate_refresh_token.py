#!/usr/bin/env python3
"""
Generate OAuth2 Refresh Token for Google Ads API

This script generates the refresh token needed for API authentication.
Run this once to get your refresh token, then store it securely.

Usage:
    python3 generate_refresh_token.py
"""

import webbrowser
from urllib.parse import urlencode, parse_qs, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json

# PhD Networks credentials
CLIENT_ID = "1093467682273-mbbq6mpeoegnnehnisahv3mcouqgoemg.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8080"
SCOPES = ["https://www.googleapis.com/auth/adwords"]

# Store the authorization code when received
auth_code = None


class OAuthHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback."""
    
    def do_GET(self):
        global auth_code
        
        # Parse the authorization code from the callback URL
        query = urlparse(self.path).query
        params = parse_qs(query)
        
        if 'code' in params:
            auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html>
                <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                    <h1 style="color: #4CAF50;">Authorization Successful!</h1>
                    <p>You can close this window and return to the terminal.</p>
                </body>
                </html>
            """)
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Authorization failed. No code received.")
    
    def log_message(self, format, *args):
        pass  # Suppress HTTP server logs


def get_authorization_url():
    """Generate the OAuth authorization URL."""
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent"  # Force consent to ensure refresh token is returned
    }
    return f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"


def exchange_code_for_tokens(code):
    """Exchange authorization code for access and refresh tokens."""
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    
    response = requests.post("https://oauth2.googleapis.com/token", data=data)
    return response.json()


def main():
    global auth_code
    
    print("=" * 60)
    print("Google Ads API - Refresh Token Generator")
    print("PhD Networks & Systems Ltd")
    print("=" * 60)
    print()
    
    # Generate and display the authorization URL
    auth_url = get_authorization_url()
    print("1. Opening browser for Google authorization...")
    print()
    print("   If the browser doesn't open automatically, visit:")
    print(f"   {auth_url}")
    print()
    
    # Try to open browser
    try:
        webbrowser.open(auth_url)
    except:
        print("   (Could not open browser automatically)")
    
    print("2. Sign in with your Google account that has access to")
    print("   the Google Ads Manager Account (490-663-7401)")
    print()
    print("3. Grant the requested permissions")
    print()
    print("Waiting for authorization...")
    print()
    
    # Start local server to receive callback
    server = HTTPServer(('localhost', 8080), OAuthHandler)
    server.handle_request()  # Handle single request
    
    if auth_code:
        print("4. Authorization code received. Exchanging for tokens...")
        print()
        
        tokens = exchange_code_for_tokens(auth_code)
        
        if 'refresh_token' in tokens:
            print("=" * 60)
            print("SUCCESS! Here are your tokens:")
            print("=" * 60)
            print()
            print(f"Refresh Token: {tokens['refresh_token']}")
            print()
            print(f"Access Token: {tokens.get('access_token', 'N/A')[:50]}...")
            print()
            print("=" * 60)
            print()
            print("IMPORTANT: Save your refresh token securely!")
            print()
            print("Add this to your google-ads.yaml config file:")
            print()
            print("---")
            print(f"developer_token: QEbSx8y0DWbQPKeR635KDg")
            print(f"client_id: {CLIENT_ID}")
            print(f"client_secret: {CLIENT_SECRET}")
            print(f"refresh_token: {tokens['refresh_token']}")
            print(f"login_customer_id: 4906637401")
            print(f"use_proto_plus: True")
            print("---")
            
            # Also save to a file
            config = {
                "developer_token": "QEbSx8y0DWbQPKeR635KDg",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "refresh_token": tokens['refresh_token'],
                "login_customer_id": "4906637401",
                "use_proto_plus": True
            }
            
            with open("google-ads-config.json", "w") as f:
                json.dump(config, f, indent=2)
            print()
            print("Config also saved to: google-ads-config.json")
            
        else:
            print("ERROR: No refresh token in response.")
            print(f"Response: {json.dumps(tokens, indent=2)}")
    else:
        print("ERROR: No authorization code received.")


if __name__ == "__main__":
    main()
