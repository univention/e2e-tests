# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

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
def user(udm, faker, email_domain, external_email_domain, user_password, cleanup):
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


# TODO: Think we only need a cleanup in development scenarios to be able to
# repeat the run and have a well known starting point.
@pytest.fixture
def cleanup():
    import subprocess

    yield

    print("Cleaning up Kubernetes state")

    import time

    time.sleep(4)

    # TODO: Restore clean state
    result = subprocess.run(
        [
            "kubectl",
            "delete",
            "pod/nubus-ldap-server-primary-1",
        ]
    )
    result.check_returncode()
    result = subprocess.run(["kubectl", "delete", "pod/nubus-ldap-server-primary-0", "--force"])
    result.check_returncode()


LABELS_ACTIVE_PRIMARY_LDAP_SERVER = {
    "app.kubernetes.io/name": "ldap-server",
    "ldap-server-type": "primary",
    # TODO: Change once leader election has been implemented
    "apps.kubernetes.io/pod-index": "0",
}


@pytest.fixture
def ldap(user):
    return LDAPFixture(user)


def test_killed_pod_triggers_transition(ldap, k8s_chaos, cleanup):
    ldap.inject_changes()
    expected_context_csn = ldap.get_context_csn()

    print("Start experiment")
    experiment = k8s_chaos.pod_kill(label_selectors=LABELS_ACTIVE_PRIMARY_LDAP_SERVER)

    print("Waiting")
    # TODO: Wait until the other Pod became the active one
    experiment.wait_until_running()
    import time

    time.sleep(60)

    print("Asserting")
    # TODO: Move retrying into the ldap fixture
    # The call to the UDM Rest API might fail a few times during the transition
    # to the hot-standby.
    assert retrying(ldap.get_context_csn)() == expected_context_csn

    print("Waiting before cleanup may start")
    time.sleep(40)

    print("done")
