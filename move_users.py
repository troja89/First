import requests
    
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


def get_role_id_by_name(role_url, headers, account_group_id, role_name):
    response = requests.get(role_url, headers=headers, params={"aid": account_group_id})
    if not response.ok:
        print("Could not fetch roles.")
        print("Status:", response.status_code)
        print("Body:", response.text)
        return None

    for role in response.json().get("roles", []):
        if role.get("name") == role_name:
            return role.get("roleId")
    return None


def get_users(api_url_users, headers, account_group_id):
    response = requests.get(api_url_users, headers=headers, params={"aid": account_group_id})
    if not response.ok:
        print("Could not fetch users.")
        print("Status:", response.status_code)
        print("Body:", response.text)
        return None

    return response.json().get("users", [])


def user_exists_in_account_group(api_url_users, headers, account_group_id, email):
    users = get_users(api_url_users, headers, account_group_id)
    if users is None:
        return False
    normalized_email = email.strip().lower()
    for user in users:
        user_email = (user.get("email") or "").strip().lower()
        if user_email == normalized_email:
            return True
    return False


def get_user_details(api_url_users, headers, account_group_id, user_id):
    response = requests.get(
        f"{api_url_users}/{user_id}",
        headers=headers,
        params={"aid": account_group_id},
    )
    if not response.ok:
        return None
    payload = response.json()
    if isinstance(payload, dict) and "users" in payload and payload["users"]:
        return payload["users"][0]
    return payload if isinstance(payload, dict) else None


def get_user_identifier(user):
    # Different endpoints/tenants may use different user ID field names.
    return (
        user.get("id")
        or user.get("userId")
        or user.get("uid")
        or user.get("accountUserId")
    )


def extract_role_data(value, role_ids, role_names):
    if isinstance(value, dict):
        for key, nested_value in value.items():
            key_lower = str(key).lower()
            if key_lower in ("roleid", "role_id"):
                role_ids.add(str(nested_value))
            elif key_lower in ("roleids", "role_ids") and isinstance(nested_value, list):
                role_ids.update(str(item) for item in nested_value)
            elif key_lower in ("rolename", "role_name"):
                role_names.add(str(nested_value).strip().lower())
            elif key_lower in ("rolenames", "role_names") and isinstance(nested_value, list):
                role_names.update(str(item).strip().lower() for item in nested_value)
            extract_role_data(nested_value, role_ids, role_names)
    elif isinstance(value, list):
        for item in value:
            extract_role_data(item, role_ids, role_names)


def get_elisa_users_by_role(
    users, source_role_id, role_name, api_url_users, headers, source_account_group_id
):
    source_role_id_str = str(source_role_id)
    role_name_lower = role_name.strip().lower()
    matching_users = []
    for user in users:
        email = (user.get("email") or "").strip().lower()
        if not email.endswith("@elisa.fi"):
            continue

        user_for_matching = user
        user_id = get_user_identifier(user)
        if user_id is not None:
            details = get_user_details(api_url_users, headers, source_account_group_id, user_id)
            if details:
                user_for_matching = details

        role_ids_str = set()
        role_names = set()
        extract_role_data(user_for_matching, role_ids_str, role_names)

        if source_role_id_str in role_ids_str or role_name_lower in role_names:
            matching_users.append(
                {
                    "email": user.get("email"),
                    "name": user.get("name") or "Unknown Name",
                }
            )
    return matching_users


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


def add_users_to_account_group(api_url_users, headers, target_account_group_id, target_role_id, users):
    success_count = 0
    warning_count = 0
    failure_count = 0
    for user in users:
        payload = create_user_payload(
            user_email=user["email"],
            user_name=user["name"],
            account_group_id=target_account_group_id,
            role_id=target_role_id,
        )
        response = requests.post(
            api_url_users,
            headers=headers,
            params={"aid": target_account_group_id},
            json=payload,
        )
        if response.ok:
            success_count += 1
            print(f"Added user: {user['email']} (activation pending user acceptance)")
        else:
            # In this tenant we can receive a 404 body even when the user is created.
            if user_exists_in_account_group(
                api_url_users, headers, target_account_group_id, user["email"]
            ):
                success_count += 1
                warning_count += 1
                print(f"Added user with API warning: {user['email']}")
                print("Status:", response.status_code)
                print("Body:", response.text)
                print("Detected in target group after request (activation pending user acceptance).")
            else:
                failure_count += 1
                print(f"Failed to add user: {user['email']}")
                print("Status:", response.status_code)
                print("Body:", response.text)
    return success_count, warning_count, failure_count


def preview_users_to_add(users):
    print("\nDRY RUN: no users will be added.")
    print(f"Users that would be added: {len(users)}")
    for user in users:
        print(f"  - {user['name']} <{user['email']}>")


if __name__ == "__main__":
    oauth_token = "01ab-7b641496-ffde-4685-86f7-a89abdf193fc"  # Replace with the current token.
    headers = {
        "Accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {oauth_token}",
    }
    api_url_users = "https://api.thousandeyes.com/v7/users"
    account_group_url = "https://api.thousandeyes.com/v7/account-groups"
    role_url = "https://api.thousandeyes.com/v7/roles"
    role_prefix = "AAD_Elisa_Tutka_"

    source_customer_name = input("Source customer name: ").strip()
    source_account_group_id = get_account_group_id(account_group_url, headers, source_customer_name)
    if not source_account_group_id:
        print(f"No account group found for '{source_customer_name}'.")
        raise SystemExit(1)

    print(f"Source account group ID: {source_account_group_id}")

    role_suffix = input("Role suffix to move (e.g. sd, noc, orgadmin): ").strip()
    role_name = f"{role_prefix}{role_suffix}"
    print(f"Using role name: {role_name}")
    source_role_id = get_role_id_by_name(role_url, headers, source_account_group_id, role_name)
    if not source_role_id:
        print(f"Role '{role_name}' not found in source account group.")
        raise SystemExit(1)

    target_customer_name = input("Target customer name (new account group): ").strip()
    target_account_group_id = get_account_group_id(account_group_url, headers, target_customer_name)
    if not target_account_group_id:
        print(f"No account group found for '{target_customer_name}'.")
        raise SystemExit(1)

    print(f"Target account group ID: {target_account_group_id}")

    target_role_id = get_role_id_by_name(role_url, headers, target_account_group_id, role_name)
    if not target_role_id:
        print(f"Role '{role_name}' not found in target account group.")
        raise SystemExit(1)

    users = get_users(api_url_users, headers, source_account_group_id)
    if users is None:
        raise SystemExit(1)

    users_to_move = get_elisa_users_by_role(
        users,
        source_role_id,
        role_name,
        api_url_users,
        headers,
        source_account_group_id,
    )
    if not users_to_move:
        print(f"No @elisa.fi users found with role '{role_name}' in source group.")
        raise SystemExit(0)

    print(f"\nFound {len(users_to_move)} @elisa.fi users with role '{role_name}':")
    for user in users_to_move:
        print(f"  - {user['name']} <{user['email']}>")

    dry_run_choice = input("\nRun in dry_run mode? (y/n): ").strip().lower()
    dry_run = dry_run_choice in ("y", "yes")

    if dry_run:
        preview_users_to_add(users_to_move)
        raise SystemExit(0)

    confirm = input("\nAdd these users to target account group now? (y/n): ").strip().lower()
    if confirm not in ("y", "yes"):
        print("Cancelled.")
        raise SystemExit(0)

    success_count, warning_count, failure_count = add_users_to_account_group(
        api_url_users=api_url_users,
        headers=headers,
        target_account_group_id=target_account_group_id,
        target_role_id=target_role_id,
        users=users_to_move,
    )

    print("\nDone.")
    print(f"Successful: {success_count}")
    print(f"Successful with API warning: {warning_count}")
    print(f"Failed: {failure_count}")