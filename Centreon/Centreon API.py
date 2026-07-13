import os
from getpass import getpass

import requests

BASE_URL = os.getenv("CENTREON_BASE_URL", "https://monitoring.santacare.net")
USERNAME = os.getenv("CENTREON_USERNAME", "toja")
PASSWORD = os.getenv("CENTREON_PASSWORD")


def login_and_fetch_hosts_beta():
    base_url = input(f"Base URL [{BASE_URL}]: ").strip() or BASE_URL
    username = input(f"Username [{USERNAME}]: ").strip() or USERNAME
    password = PASSWORD or getpass("Password: ").strip()
    if not password:
        raise RuntimeError("Password is required.")

    login_url = f"{base_url}/centreon/api/beta/login"
    payload = {
        "security": {
            "credentials": {
                "login": username,
                "password": password,
            }
        }
    }

    # Login
    resp = requests.post(login_url, json=payload)
    print("Login status:", resp.status_code)
    print("Login raw body:", resp.text)
    resp.raise_for_status()

    data = resp.json()
    print("Login JSON:", data)

    # Many Centreon versions return a token you then pass as Bearer.
    # Adjust this access if the structure is different.
    token = data["security"]["token"]
    print("Token (for debug):", token)

    headers = {
        "X-AUTH-TOKEN": token,
        "Accept": "application/json",
    }

    # Example: list hosts in beta API (adjust path/permissions for your version)
    hosts_url = f"{base_url}/centreon/api/beta/monitoring/hosts"
    hosts_resp = requests.get(hosts_url, headers=headers)
    print("Hosts status:", hosts_resp.status_code)
    print("Hosts raw body:", hosts_resp.text)

    try:
        hosts_resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Hosts request failed:", e)
        return

    print("Login OK, hosts response JSON:")
    print(hosts_resp.json())


if __name__ == "__main__":
    login_and_fetch_hosts_beta()


def get_api_data(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        if "response" in locals() and response is not None:
            print(response.text)
        return None










