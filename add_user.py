import requests
import json

def get_account_group_id(account_group_url, headers, customer_name):
    response = requests.get(account_group_url, headers=headers)
    if not response.ok:
        print("Could not fetch account groups.")
        print("Status:", response.status_code)
        print("Body:", response.text)
        return None

    account_groups = response.json().get("accountGroups", [])
    for group in account_groups:
        if group.get("accountGroupName") == customer_name:
            return group.get("aid")
    return None


def get_role_id(role_url, headers, account_group_id, role_name):
    response = requests.get(role_url, headers=headers, params={"aid": account_group_id})
    if not response.ok:
        print("Could not fetch roles.")
        print("Status:", response.status_code)
        print("Body:", response.text)
        return None

    roles = response.json().get("roles", [])
    for role in roles:
        if role.get("name") == role_name:
            return role.get("roleId")
    return None


def create_user_payload(user_email, user_name, account_group_id, role_id):
    return {
        "email": user_email,
        "name": user_name,
        "loginAccountGroupId": account_group_id,
        "accountGroupRoles": [
            {"accountGroupId": account_group_id, "roleIds": [role_id]}
        ],
        "allAccountGroupRoleIds": [role_id],
    }


def generate_name_from_email(email):
    local_part = email.split("@", 1)[0]
    cleaned = local_part.replace(".", " ").replace("_", " ").replace("-", " ")
    parts = [part for part in cleaned.split() if part]
    if not parts:
        return "Unknown User"
    return " ".join(part.capitalize() for part in parts)


def parse_users_input(raw_input):
    users = []
    entries = [entry.strip() for entry in raw_input.split(",") if entry.strip()]
    for entry in entries:
        if "|" in entry:
            email, name = entry.split("|", 1)
            email = email.strip()
            name = name.strip()
        else:
            email = entry.strip()
            name = generate_name_from_email(email)

        if "@" not in email:
            print(f"Skipping '{entry}' - invalid email format.")
            continue
        if not name:
            name = generate_name_from_email(email)
        users.append((email, name))
    return users


if __name__ == "__main__":
    oauth_token = "01ab-7ae13326-63e6-4b6d-ba99-158c71e05a46"  # Replace with the current token.
    headers = {
        "Accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {oauth_token}",
    }
    api_url_users = "https://api.thousandeyes.com/v7/users"
    account_group_url = "https://api.thousandeyes.com/v7/account-groups"
    role_url = "https://api.thousandeyes.com/v7/roles"

    customer_name = input("What is the customer name? ")
    account_group_id = get_account_group_id(account_group_url, headers, customer_name)
    if not account_group_id:
        print(f"No account group found for '{customer_name}'.")
        raise SystemExit(1)

    print(f"Account Group ID: {account_group_id}")
    role_name = input(
        "What is the role name? "
        "(AAD_Elisa_Tutka_noc, AAD_Elisa_Tutka_accountadmin, "
        "AAD_Elisa_Tutka_orgadmin, AAD_Elisa_Tutka_sd, AAD_Elisa_Tutka_user) "
    )
    role_id = get_role_id(role_url, headers, account_group_id, role_name)
    if not role_id:
        print(f"No role found for '{role_name}'.")
        raise SystemExit(1)

    print(f"Role ID: {role_id}")

    # Loop to add multiple users in one run.
    while True:
        users_input = input(
            "\nEnter users as comma-separated values using either 'email|name' or plain 'email'\n"
            "Example: user1@email.com|User One, user2@email.com, john_doe@email.com\n"
            "Users: "
        ).strip()
        users_to_create = parse_users_input(users_input)

        if not users_to_create:
            print("No valid users provided.")
        for user_email, user_name in users_to_create:
            user = create_user_payload(user_email, user_name, account_group_id, role_id)

            print("\nSubmitting user payload:")
            print(json.dumps(user, indent=2))

            response = requests.post(
                api_url_users, json=user, headers=headers, params={"aid": account_group_id}
            )
            if response.ok:
                print(f"User '{user_email}' created successfully.")
                print(response.json())
            else:
                print(f"Request failed for '{user_email}'.")
                print("Status:", response.status_code)
                print("Body:", response.text)
                try:
                    print("JSON:", response.json())
                except ValueError:
                    pass

        add_another = input("\nAdd another user? (y/n): ").strip().lower()
        if add_another not in ("y", "yes"):
            print("Done.")
            break