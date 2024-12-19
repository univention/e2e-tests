# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH
import random
import string
from typing import List

import ldap3
import ldap3.core.exceptions


def generate_random_string(length: int = 8) -> str:
    """Generate a random string of specified length."""
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def create_initial_groups(ldap, ldap_conn, num_groups: int) -> List[str]:
    """Create initial groups in LDAP."""
    print("\nCreating initial groups...")

    # Create dummy user
    print("Creating dummy user for initial group membership...")
    dummy_user_attrs = {
        "objectClass": ["top", "inetOrgPerson"],
        "cn": ["dummy"],
        "sn": ["user"],
        "mail": ["dummy@example.com"],
        "userPassword": ["password"],
    }
    dummy_user_dn = "cn=dummy,cn=users," + ldap.base_dn
    try:
        ldap_conn.add(dummy_user_dn, "inetOrgPerson", dummy_user_attrs)
        print("Dummy user created successfully")
    except ldap3.core.exceptions.LDAPException as e:
        print(f"Error creating dummy user: {e}")
        raise

    groups = []
    print(f"Creating {num_groups} groups...")
    for i in range(num_groups):
        group_name = f"test-group-{i}"
        group_dn = f"cn={group_name},cn=groups,{ldap.base_dn}"
        group_attrs = {
            "objectClass": ["top", "groupOfNames"],
            "cn": [group_name],
            "member": ["cn=dummy,cn=users," + ldap.base_dn],
        }
        try:
            ldap_conn.add(group_dn, "groupOfNames", group_attrs)
            groups.append(group_dn)
            if (i + 1) % 10 == 0:  # Progress indicator every 10 groups
                print(f"Created {i + 1}/{num_groups} groups")
        except ldap3.core.exceptions.LDAPException as e:
            print(f"Error creating group {group_name}: {e}")
            raise RuntimeError(f"Failed to create group {group_name}: {e}")

    print(f"Successfully created {len(groups)} groups")
    return groups


def create_initial_users(ldap, ldap_conn, num_users: int) -> List[str]:
    """Create initial users in LDAP."""
    print(f"\nCreating {num_users} users...")
    users = []
    for i in range(num_users):
        username = f"test-user-{i}"
        user_dn = f"uid={username},cn=users,{ldap.base_dn}"
        user_attrs = {
            "objectClass": ["top", "person", "organizationalPerson", "inetOrgPerson"],
            "uid": [username],
            "cn": [username],
            "sn": [f"User{i}"],
            "userPassword": [generate_random_string()],
        }
        try:
            ldap_conn.add(user_dn, "inetOrgPerson", user_attrs)
            users.append(user_dn)
            if (i + 1) % 10 == 0:  # Progress indicator every 10 users
                print(f"Created {i + 1}/{num_users} users")
        except ldap3.core.exceptions.LDAPException as e:
            print(f"Error creating user {username}: {e}")
            raise RuntimeError(f"Failed to create user {username}: {e}")

    print(f"Successfully created {len(users)} users")
    return users


def assign_random_users_to_groups(
    ldap_conn, users: List[str], groups: List[str], min_groups_per_user: int = 1, max_groups_per_user: int = 5
):
    """Randomly assign users to groups."""
    print(f"\nAssigning users to groups (min: {min_groups_per_user}, max: {max_groups_per_user} groups per user)...")
    total_assignments = 0

    for i, user_dn in enumerate(users):
        num_groups = random.randint(min_groups_per_user, max_groups_per_user)
        selected_groups = random.sample(groups, num_groups)

        for group_dn in selected_groups:
            try:
                ldap_conn.modify(group_dn, {"member": [ldap3.MODIFY_ADD, [user_dn]]})
                total_assignments += 1
            except ldap3.core.exceptions.LDAPException as e:
                if e.args[0]["desc"] != "Type or value exists":
                    print(f"Error adding user {user_dn} to group {group_dn}: {e}")
                    raise RuntimeError(f"Failed to add user {user_dn} to group {group_dn}: {e}")

        if (i + 1) % 10 == 0:  # Progress indicator every 10 users
            print(f"Processed {i + 1}/{len(users)} users")

    print(f"Successfully completed {total_assignments} group assignments")


def move_random_users_between_groups(env, ldap_conn, users: List[str], groups: List[str], num_users: int):
    """
    Move random users between groups and return the changes made.

    Args:
        ldap_conn: LDAP connection
        users: List of user DNs
        groups: List of group DNs
        num_users: Number of users to move

    Returns:
        dict: A dictionary tracking all changes made, in the format:
            {
                'group_dn': {
                    'added': set(user_dns),
                    'removed': set(user_dns)
                }
            }
    """
    print(f"\nMoving {num_users} users between groups...")
    selected_users = random.sample(users, num_users)
    total_moves = 0
    changes = {}  # Track all changes made

    for i, user_dn in enumerate(selected_users):
        print(f"\nProcessing user {i + 1}/{num_users}: {user_dn}")

        # Get current groups
        current_groups = get_user_groups(env, ldap_conn, user_dn)
        print(f"Current group membership: {len(current_groups)} groups")

        # Remove from some current groups
        if current_groups:
            num_groups_to_remove = random.randint(1, len(current_groups))
            groups_to_remove = random.sample(current_groups, num_groups_to_remove)
            print(f"Removing user from {len(groups_to_remove)} groups")

            for group_dn in groups_to_remove:
                try:
                    ldap_conn.modify(group_dn, {"member": [ldap3.MODIFY_DELETE, [user_dn]]})
                    total_moves += 1

                    # Track removal
                    if group_dn not in changes:
                        changes[group_dn] = {"removed": set(), "added": set()}
                    changes[group_dn]["removed"].add(user_dn)

                except ldap3.core.exceptions.LDAPException as e:
                    print(f"Error removing user from group {group_dn}: {e}")
                    raise RuntimeError(f"Failed to remove user {user_dn} from group {group_dn}: {e}")

        # Add to new groups
        available_groups = list(set(groups) - set(current_groups))
        if available_groups:
            num_new_groups = random.randint(1, min(3, len(available_groups)))
            new_groups = random.sample(available_groups, num_new_groups)
            print(f"Adding user to {len(new_groups)} new groups")

            for group_dn in new_groups:
                try:
                    ldap_conn.modify(group_dn, {"member": [ldap3.MODIFY_ADD, [user_dn]]})
                    total_moves += 1

                    # Track addition
                    if group_dn not in changes:
                        changes[group_dn] = {"removed": set(), "added": set()}
                    changes[group_dn]["added"].add(user_dn)

                except ldap3.core.exceptions.LDAPException as e:
                    print(f"Error adding user to group {group_dn}: {e}")
                    raise RuntimeError(f"Failed to add user {user_dn} to group {group_dn}: {e}")

    print(f"Successfully completed {total_moves} group membership changes")

    # Print summary of changes
    print("\nChange Summary:")
    for group_dn, group_changes in changes.items():
        print(f"\nGroup: {group_dn}")
        print(f"  - Added {len(group_changes['added'])} users")
        print(f"  - Removed {len(group_changes['removed'])} users")

    return changes


def get_user_groups(ldap, ldap_conn, user_dn: str) -> List[str]:
    """Get all groups a user belongs to."""
    try:
        search_filter = f"(&(objectClass=groupOfNames)(member={user_dn}))"
        ldap_conn.search(f"cn=groups,{ldap.base_dn}", search_filter, ldap3.SUBTREE, attributes=[])
        return [item["dn"] for item in ldap_conn.response]
    except ldap3.core.exceptions.LDAPException as e:
        print(f"Error getting groups for user {user_dn}: {e}")
        raise RuntimeError(f"Failed to get groups for user {user_dn}: {e}")
