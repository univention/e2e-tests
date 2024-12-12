# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging
import time
from e2e.ldap import LDAPFixture

import pytest


log = logging.getLogger(__name__)

LABELS_ACTIVE_PRIMARY_LDAP_SERVER = {
    "app.kubernetes.io/name": "ldap-server",
    "ldap-server-type": "primary",
    "ldap-leader": "true",
}


def test_new_leader_has_correct_context_csn(faker, ldap: LDAPFixture, k8s_chaos):
    context_csn = ldap.get_context_csn()
    log.debug("contextCSN initial state: %s", context_csn)

    k8s_chaos.pod_kill(label_selectors=LABELS_ACTIVE_PRIMARY_LDAP_SERVER)

    wait_until(ldap.all_primaries_reachable, False, timeout=5)
    log.info("One ldap primary became unreachable.")

    primary = ldap.get_server(role="primary")
    conn = primary.conn

    create_and_delete_a_ldap_entry(faker, conn)

    expected_context_csn = primary.get_context_csn()

    wait_until(ldap.all_primaries_reachable, True, timeout=40)
    log.info("Both ldap primary servers are reachable again.")

    # TODO: Expect the contextCSN to eventually converge
    # TODO: Expect the resulting contextCSN to be the one from after the write
    print(expected_context_csn)
    found_context_csn = ldap.get_context_csn()

    assert [expected_context_csn, expected_context_csn] == list(found_context_csn.values())


    assert False, "finish me!"


def create_and_delete_a_ldap_entry(faker, conn):
    base_dn = "dc=univention-organization,dc=intranet"
    users_container_dn = f"cn=users,{base_dn}"

    user_uid = faker.user_name()
    user_dn = f"uid={user_uid},{users_container_dn}"
    user_attributes = {
        "cn": faker.name(),
        "sn": faker.last_name(),
    }

    with conn:
        conn.add(user_dn, "inetOrgPerson", user_attributes)
        conn.delete(user_dn)


def wait_until(func, expected, timeout=10):
    for _ in range(timeout):
        if func() == expected:
            break
        log.debug("Waiting until %s is %s", func, expected)
        time.sleep(1)
    else:
        raise Exception("Timed out in wait_until.")
