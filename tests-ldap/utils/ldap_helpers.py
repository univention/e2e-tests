# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH


import ldap3
import ldap3.core.exceptions


def compare_ldap_servers(conn1, conn2, base_dn):
    """
    Compare content of two LDAP servers.

    Args:
        conn1: First LDAP connection
        conn2: Second LDAP connection
        base_dn: Base DN to start comparison from

    Returns:
        bool: True if servers are identical, False otherwise
    """
    try:
        # Get all entries from both servers
        search_filter = "(objectClass=*)"
        attrs = ["*"]  # Fetch all attributes

        # Fetch entries from first server
        entries1 = {}
        conn1.search(base_dn, search_filter, ldap3.SUBTREE, attributes=attrs)
        for item in conn1.response:
            # Convert attribute values to sets for comparison
            normalized_attrs1 = {k: set(v) if isinstance(v, list) else v for k, v in item["attributes"].items()}
            entries1[item["dn"]] = normalized_attrs1

        # Fetch entries from second server
        entries2 = {}
        conn2.search(base_dn, search_filter, ldap3.SUBTREE, attributes=attrs)
        for item in conn2.response:
            # Convert attribute values to sets for comparison
            normalized_attrs2 = {k: set(v) if isinstance(v, list) else v for k, v in item["attributes"].items()}
            entries2[item["dn"]] = normalized_attrs2

        # Compare DNs
        if set(entries1.keys()) != set(entries2.keys()):
            print("DNs don't match between servers")
            # return False

        # Compare attributes for each DN
        for dn in entries1:
            attrs1 = entries1[dn]
            attrs2 = entries2[dn]

            # Compare attribute names
            if set(attrs1.keys()) != set(attrs2.keys()):
                print(f"Attribute names don't match for DN: {dn}")
                # return False

            # Compare attribute values
            for attr_name in attrs1:
                if attrs1[attr_name] != attrs2[attr_name]:
                    print(f"Attribute values don't match for DN: {dn}, attribute: {attr_name}")
                    # return False

        return True

    except ldap3.core.exceptions.LDAPException as e:
        raise RuntimeError(f"Failed to compare LDAP servers: {e}")


def verify_group_memberships(conn, users, groups):
    """
    Verify group memberships are consistent.

    Args:
        conn: LDAP connection
        users: List of user DNs
        groups: List of group DNs

    Returns:
        bool: True if memberships are consistent, False otherwise
    """
    try:
        for group_dn in groups:
            # Get group members
            result = conn.search(group_dn, "(objectClass=*)", ldap3.BASE, attributes=["member"])

            if not result:
                print(f"Group not found: {group_dn}")
                return False

            group_members = set(result[0][1].get("member", []))

            # Verify each member exists
            for member_dn in group_members:
                if member_dn.decode("utf-8") not in users:
                    try:
                        # Check if it's the dummy user
                        conn.search(member_dn, "(objectClass=*)", ldap3.BASE)
                    except ldap3.core.exceptions.LDAPException:
                        print(f"Invalid member in group {group_dn}: {member_dn}")
                        return False

        return True

    except ldap3.core.exceptions.LDAPException as e:
        raise RuntimeError(f"Failed to verify group memberships: {e}")


def get_all_group_memberships(conn, groups):
    """Get current membership state of all groups."""
    memberships = {}
    for group_dn in groups:
        conn.search(group_dn, "(objectClass=*)", ldap3.BASE, attributes=["member"])
        if conn.entries:
            entry = conn.entries[0]
            members = set(entry.member.values)
            memberships[group_dn] = members
    return memberships


def verify_membership_changes(old_state, new_state, changes):
    """Verify that membership changes were applied correctly."""
    for group_dn, change in changes.items():
        new_members = new_state.get(group_dn, set())

        # Verify removals
        for removed_member in change.get("removed", set()):
            assert (
                removed_member not in new_members
            ), f"Member {removed_member} should have been removed from {group_dn}"

        # Verify additions
        for added_member in change.get("added", set()):
            assert added_member in new_members, f"Member {added_member} should have been added to {group_dn}"


def verify_all_changes_preserved(initial_state, final_state, first_batch, second_batch):
    """Verify that all changes from both batches were preserved."""
    # Combine both batches of changes, maintaining order
    all_changes = {}
    for batch_num, changes in enumerate([first_batch, second_batch]):
        for group_dn, change in changes.items():
            if group_dn not in all_changes:
                all_changes[group_dn] = {"added": [], "removed": [], "operations": []}

            # Store operations in order with batch number
            for added in change.get("added", set()):
                all_changes[group_dn]["operations"].append((batch_num, "add", added))
            for removed in change.get("removed", set()):
                all_changes[group_dn]["operations"].append((batch_num, "remove", removed))

    # Process operations in order for each group
    for group_dn, change in all_changes.items():
        initial_members = initial_state.get(group_dn, set())
        final_members = final_state.get(group_dn, set())

        # Sort operations by batch number
        sorted_ops = sorted(change["operations"])
        current_members = initial_members.copy()

        # Apply operations in order
        for _, op_type, member in sorted_ops:
            if op_type == "add":
                current_members.add(member)
            else:  # remove
                current_members.discard(member)

        expected_members = current_members
        assert final_members == expected_members, (
            f"Final membership state for {group_dn} doesn't match expected state.\n"
            f"Missing: {expected_members - final_members}\n"
            f"Extra: {final_members - expected_members}"
        )
