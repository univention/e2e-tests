# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import time

import ldap3
import ldap3.core.exceptions
import pytest
from utils.data_generators import (
    assign_random_users_to_groups,
    create_initial_groups,
    create_initial_users,
    move_random_users_between_groups,
)
from utils.k8s_helpers import delete_pod, delete_pod_pvc, wait_for_pod_ready
from utils.ldap_helpers import (
    compare_ldap_servers,
    get_all_group_memberships,
    verify_all_changes_preserved,
    verify_membership_changes,
)

from e2e.ldap import LdapDeployment

# Test configurations
NUM_GROUPS = 10
NUM_USERS = 100
NUM_USERS_TO_MOVE = 50


@pytest.fixture
def cleanup_ldap(ldap: LdapDeployment):
    """Cleanup LDAP data after tests."""
    yield
    conn_primary = ldap.get_server_for_primary_service().connect(bind=True)

    # Delete test users
    print("Deleting test users")
    user_filter = "(uid=test-user-*)"
    conn_primary.search(f"cn=users,{ldap.base_dn}", user_filter, ldap3.LEVEL)
    for item in conn_primary.response:
        try:
            conn_primary.delete(item["dn"])
        except ldap3.core.exceptions.LDAPException:
            pass

    # Delete test groups
    print("Deleting test groups")
    group_filter = "(cn=test-group-*)"
    conn_primary.search(f"cn=groups,{ldap.base_dn}", group_filter, ldap3.LEVEL)
    for item in conn_primary.response:
        try:
            conn_primary.delete(item["dn"])
        except ldap3.core.exceptions.LDAPException:
            pass

    # Delete dummy user if it exists
    try:
        print("Deleting dummy user")
        conn_primary.delete(f"cn=dummy,cn=users,{ldap.base_dn}")
    except ldap3.core.exceptions.LDAPException:
        pass

    print("Finished cleanup")


@pytest.mark.usefixtures("cleanup_ldap")
def test_ldap_mirror_mode_robustness(k8s, k8s_api, ldap: LdapDeployment):
    """Test LDAP mirror mode robustness under pod failure."""
    print("\n=== Starting LDAP Mirror Mode Robustness Test ===")

    print("Getting initial connections to LDAP servers...")
    conn_primary_0 = ldap.servers["primary_0"].connect(bind=True, client_strategy="RESTARTABLE")
    conn_primary_1 = ldap.servers["primary_1"].connect(bind=True, client_strategy="RESTARTABLE")
    print("Successfully connected to both LDAP servers")

    print(f"\nCreating initial state with {NUM_GROUPS} groups...")
    groups = create_initial_groups(ldap, conn_primary_0, NUM_GROUPS)
    print(f"Successfully created {len(groups)} groups")

    print(f"\nCreating {NUM_USERS} users...")
    users = create_initial_users(ldap, conn_primary_0, NUM_USERS)
    print(f"Successfully created {len(users)} users")

    print("\nAssigning random users to groups...")
    assign_random_users_to_groups(conn_primary_0, users, groups)
    print("Successfully assigned users to groups")

    print("\nVerifying initial state replication between servers...")
    assert compare_ldap_servers(conn_primary_0, conn_primary_1, ldap.base_dn)
    print("Initial state verification successful")

    # Track initial group memberships
    initial_memberships = get_all_group_memberships(conn_primary_0, groups)

    print(f"\nMoving first batch of {NUM_USERS_TO_MOVE} users between groups...")
    first_batch_changes = move_random_users_between_groups(ldap, conn_primary_0, users, groups, NUM_USERS_TO_MOVE)

    # Verify first batch changes were applied
    first_batch_memberships = get_all_group_memberships(conn_primary_0, groups)
    verify_membership_changes(initial_memberships, first_batch_memberships, first_batch_changes)

    print(f"\nDeleting PVC and killing pod: {ldap.primary_0_pod_name}")
    delete_pod_pvc(k8s_api, ldap.primary_0_pod_name, k8s.namespace)
    delete_pod(k8s_api, ldap.notifier_pod_name, k8s.namespace)

    print(f"\nMoving second batch of {NUM_USERS_TO_MOVE} users between groups...")
    second_batch_changes = move_random_users_between_groups(ldap, conn_primary_1, users, groups, NUM_USERS_TO_MOVE)

    # Verify second batch changes were applied to primary-1
    intermediate_memberships = get_all_group_memberships(conn_primary_1, groups)
    verify_membership_changes(first_batch_memberships, intermediate_memberships, second_batch_changes)

    print("\nWaiting for deleted pod to come back...")
    wait_for_pod_ready(k8s_api, ldap.primary_0_pod_name, k8s.namespace)
    print("\nWaiting additional 10 seconds for sync...")
    time.sleep(10)

    print("Getting fresh connection to primary-0...")
    conn_primary_0 = ldap.servers["primary_0"].connect(bind=True, client_strategy="RESTARTABLE")

    print("\nVerifying final state...")
    # Verify both servers have identical state
    assert compare_ldap_servers(conn_primary_0, conn_primary_1, ldap.base_dn)

    # Verify all changes were preserved
    final_memberships = get_all_group_memberships(conn_primary_0, groups)
    verify_all_changes_preserved(initial_memberships, final_memberships, first_batch_changes, second_batch_changes)

    print("\n=== LDAP Mirror Mode Robustness Test Completed Successfully ===")
