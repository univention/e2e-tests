# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import time

import pytest

from e2e.decorators import retrying
from e2e.ldap import LDAPFixture

# TODO: The fixtures are duplicated from the portal conftest and should be
# unified again.
#
# Be aware: The wait for the secondaries to catch up is not needed here. This
# will require a little bit of tweaking.


@pytest.fixture
def user_password(faker):
    """
    The password used for the fixture ``user``.

    This is split out so that it can be accessed easily. The UDM object
    ``user`` does not contain the password itself anymore.
    """
    return faker.password()


@pytest.fixture
def user(udm, faker, email_domain, external_email_domain, user_password):
    """
    A regular user.

    The user will be created for the test case and removed after the test case.

    The password is available in the fixture ``user_password``.
    """
    users_user = udm.get("users/user")
    test_user = users_user.new()
    username = f"test-{faker.user_name()}"

    test_user.properties.update(
        {
            "firstname": faker.first_name(),
            "lastname": faker.last_name(),
            "username": username,
            "displayName": faker.name(),
            "password": user_password,
            "mailPrimaryAddress": f"{username}@{email_domain}",
            "PasswordRecoveryEmail": f"{username}@{external_email_domain}",
        }
    )
    test_user.save()

    print("Made test user", test_user.properties["displayName"], test_user.dn)
    yield test_user

    print("Cleaning up test user", test_user.properties["displayName"], test_user.dn)
    test_user.reload()
    test_user.delete()


LABELS_ACTIVE_PRIMARY_LDAP_SERVER = {
    "app.kubernetes.io/name": "ldap-server",
    "ldap-server-type": "primary",
    "ldap-leader": "true",
}


@pytest.fixture
def ldap():
    return LDAPFixture()


def test_ldap_connection():
    from ldap3 import ALL, Connection, Server

    server = Server(
        host=f"ldap://localhost",
        port=8389,
        get_info="ALL",
        connect_timeout=1,
    )
    connection = Connection(
        server,
        user="cn=admin,dc=univention-organization,dc=intranet",
        password="univention",
        client_strategy="SYNC",
    )

    with connection:
        connection.search(
            "dc=univention-organization,dc=intranet",
            "(objectClass=*)",
            search_scope="BASE",
            attributes=["contextCSN"],
        )
        context_csn = connection.entries[0].contextCSN.value
        print(context_csn)

    # import pdb; pdb.set_trace()
    assert False, "finish me!"


def test_new_leader_has_correct_context_csn(ldap, k8s_chaos):
    context_csn = ldap.get_context_csn()
    print(context_csn)

    k8s_chaos.pod_kill(label_selectors=LABELS_ACTIVE_PRIMARY_LDAP_SERVER)

    # TODO: Wait until the pod is not reachable anymore
    time.sleep(3)

    # TODO: Trigger a change
    primary = ldap.get_connection(role="primary")
    conn = primary.conn

    try:
        with conn:
            pass
    except:
        time.sleep(3)

    with conn:
        pass

    assert False, "continue"

    # TODO: Expect both servers to eventually be reachable
    # TODO: Expect the contextCSN to eventually converge
    for x in range(400):
        print(x, ldap.get_context_csn())
        time.sleep(1)

    assert False, "finish me!"


def test_killed_pod_triggers_transition(ldap, k8s_chaos):
    assert False, "remove me"
    ldap.inject_changes()
    expected_context_csn = ldap.get_context_csn()

    experiment = k8s_chaos.pod_kill(label_selectors=LABELS_ACTIVE_PRIMARY_LDAP_SERVER)

    # TODO: Wait until the other Pod became the active one
    experiment.wait_until_running()
    time.sleep(30)

    # TODO: Move retrying into the ldap fixture
    # The call to the UDM Rest API might fail a few times during the transition
    # to the hot-standby.
    assert retrying(ldap.get_context_csn)() == expected_context_csn
