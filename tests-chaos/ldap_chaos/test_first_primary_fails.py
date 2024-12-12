# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging
import time

import pytest


log = logging.getLogger(__name__)

LABELS_ACTIVE_PRIMARY_LDAP_SERVER = {
    "app.kubernetes.io/name": "ldap-server",
    "ldap-server-type": "primary",
    "ldap-leader": "true",
}


def test_new_leader_has_correct_context_csn(faker, ldap, k8s_chaos):
    context_csn = ldap.get_context_csn()
    log.debug("contextCSN initial state: %s", context_csn)

    k8s_chaos.pod_kill(label_selectors=LABELS_ACTIVE_PRIMARY_LDAP_SERVER)

    for x in range(5):
        log.debug("Awaiting ldap primary server to become unreachable %s", x)
        if not ldap.all_servers_reachable(role="primary"):
            break
        time.sleep(1)
    else:
        raise Exception("No LDAP server became unreachable.")
    log.info("One ldap primary became unreachable.")

    primary = ldap.get_server(role="primary")
    conn = primary.conn

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

    context_csn_after_change = ldap.get_context_csn()
    log.debug("cotextCSN after change: %s", context_csn_after_change)

    for expected_context_csn in context_csn_after_change.values():
        if expected_context_csn:
            break
    else:
        raise Exception("Retrieving the expected contextCSN failed.")


    for x in range(40):
        log.debug("Awaiting ldap primary servers to become reachable again %s", x)
        if ldap.all_servers_reachable(role="primary"):
            break
        time.sleep(1)
    else:
        raise Exception("Timeout, ldap primary servers did not become reachable again.")
    log.info("Both ldap primary servers are reachable again.")

    # TODO: Expect the contextCSN to eventually converge
    # TODO: Expect the resulting contextCSN to be the one from after the write
    print(expected_context_csn)
    found_context_csn = ldap.get_context_csn()

    assert [expected_context_csn, expected_context_csn] == list(found_context_csn.values())


    assert False, "finish me!"
