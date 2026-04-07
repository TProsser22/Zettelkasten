"""
Send Zettelkasten card suggestions via Microsoft Graph API.

Usage:
    python send_email.py --subject "Zettelkasten: Card Title" --body "Email body text"

Requires:
    - GRAPH_CLIENT_ID env var (Azure App Registration client ID)
    - GRAPH_TENANT_ID env var (set to "consumers" for personal Outlook)
    - First run will prompt for interactive login and cache the token.

Install dependencies:
    pip install msal requests
"""

import argparse
import json
import os
import sys
from pathlib import Path

import msal
import requests

TOKEN_CACHE_PATH = Path(__file__).parent / ".token_cache.json"

CLIENT_ID = os.environ.get("GRAPH_CLIENT_ID", "")
TENANT_ID = os.environ.get("GRAPH_TENANT_ID", "consumers")
SCOPES = ["Mail.Send"]
GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0"


def get_msal_app():
    cache = msal.SerializableTokenCache()
    if TOKEN_CACHE_PATH.exists():
        cache.deserialize(TOKEN_CACHE_PATH.read_text())

    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        token_cache=cache,
    )
    return app, cache


def get_access_token():
    app, cache = get_msal_app()

    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            return result["access_token"]

    # Interactive login required on first use
    result = app.acquire_token_interactive(scopes=SCOPES)

    if "access_token" not in result:
        print(f"Authentication failed: {result.get('error_description', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)

    # Persist token cache
    if cache.has_state_changed:
        TOKEN_CACHE_PATH.write_text(cache.serialize())

    return result["access_token"]


def send_email(subject: str, body: str):
    if not CLIENT_ID:
        print("Error: GRAPH_CLIENT_ID environment variable not set.", file=sys.stderr)
        print("Set it to your Azure App Registration client ID.", file=sys.stderr)
        sys.exit(1)

    token = get_access_token()

    # Send to self (authenticated user)
    me_response = requests.get(
        f"{GRAPH_ENDPOINT}/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    me_response.raise_for_status()
    my_email = me_response.json().get("mail") or me_response.json().get("userPrincipalName")

    message = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body,
            },
            "toRecipients": [
                {"emailAddress": {"address": my_email}}
            ],
        }
    }

    response = requests.post(
        f"{GRAPH_ENDPOINT}/me/sendMail",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        data=json.dumps(message),
    )
    response.raise_for_status()
    print(f"Email sent to {my_email}: {subject}")


def main():
    parser = argparse.ArgumentParser(description="Send Zettelkasten suggestion email")
    parser.add_argument("--subject", required=True, help="Email subject line")
    parser.add_argument("--body", required=True, help="Email body text")
    args = parser.parse_args()

    send_email(args.subject, args.body)


if __name__ == "__main__":
    main()
