# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging

import pytest

from e2e.ldap import LdapDeployment
from e2e.util import wait_until

log = logging.getLogger(__name__)

LDAP_READY_TIMEOUT = 120
POD_REMOVED_TIMEOUT = 5


@pytest.fixture(autouse=True)
def wait_until_ready(ldap):
    """
    Ensures that the openldap servers are ready before running the tests.
    """
    wait_until(ldap.all_primaries_reachable, True, timeout=LDAP_READY_TIMEOUT)
    log.info("All ldap servers are reachable.")


def test_correct_context_csn_after_leader_switch(faker, ldap: LdapDeployment, k8s_chaos):
    k8s_chaos.pod_kill(label_selectors=ldap.LABELS_ACTIVE_PRIMARY_LDAP_SERVER)
    wait_until(ldap.all_primaries_reachable, False, timeout=POD_REMOVED_TIMEOUT)

    primary = ldap.get_server_for_primary_service()
    conn = primary.connect()
    create_and_delete_a_ldap_entry(faker, conn, ldap.users_container_dn)
    expected_context_csn = [primary.get_context_csn()] * 2

    wait_until(ldap.all_primaries_reachable, True, timeout=LDAP_READY_TIMEOUT)
    found_context_csn = list(ldap.get_context_csn().values())
    assert expected_context_csn == found_context_csn


def test_new_leader_has_correct_context_csn(faker, ldap: LdapDeployment, k8s_chaos):
    primary = ldap.get_server_for_primary_service()
    conn = primary.connect()

    create_and_delete_a_ldap_entry(faker, conn, ldap.users_container_dn)
    expected_context_csn = primary.get_context_csn()
    k8s_chaos.pod_kill(label_selectors=ldap.LABELS_ACTIVE_PRIMARY_LDAP_SERVER)
    wait_until(ldap.all_primaries_reachable, False, timeout=POD_REMOVED_TIMEOUT)

    found_context_csn = list(filter(None, ldap.get_context_csn().values()))
    assert len(found_context_csn) == 1, "Expected that only one ldap server is reachable"
    assert expected_context_csn == found_context_csn[0]


def test_write_during_leader_switch(faker, ldap: LdapDeployment, k8s_chaos):
    primary = ldap.get_server_for_primary_service()
    conn = primary.connect()

    create_and_delete_a_ldap_entry(faker, conn, ldap.users_container_dn)
    k8s_chaos.pod_kill(label_selectors=ldap.LABELS_ACTIVE_PRIMARY_LDAP_SERVER)
    create_and_delete_a_ldap_entry(faker, conn, ldap.users_container_dn)
    wait_until(ldap.all_primaries_reachable, False, timeout=POD_REMOVED_TIMEOUT)
    create_and_delete_a_ldap_entry(faker, conn, ldap.users_container_dn)
    wait_until(ldap.all_primaries_reachable, True, timeout=LDAP_READY_TIMEOUT)
    create_and_delete_a_ldap_entry(faker, conn, ldap.users_container_dn)

    expected_context_csn = [primary.get_context_csn()] * 2
    found_context_csn = list(ldap.get_context_csn().values())
    assert expected_context_csn == found_context_csn


def create_and_delete_a_ldap_entry(faker, conn, users_container_dn):
    user_uid = faker.user_name()
    user_dn = f"uid={user_uid},{users_container_dn}"
    user_attributes = {
        "cn": faker.name(),
        "sn": faker.last_name(),
    }

    with conn:
        conn.add(user_dn, "inetOrgPerson", user_attributes)
        conn.delete(user_dn)
