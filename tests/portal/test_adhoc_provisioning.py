# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import base64
from uuid import uuid4

import pytest

from e2e.ad_hoc import AdHocProvisioning
from e2e.decorators import retrying_slow
from umspages.common.base import expect
from umspages.portal.login_page import LoginPage


@pytest.fixture
def setup_ad_hoc_provisioning(
    keycloak_base_url, keycloak_admin_username, keycloak_admin_password, admin_username, admin_password, portal_base_url
):
    ad_hoc_provisioning = AdHocProvisioning(
        keycloak_url=keycloak_base_url,
        admin_username=keycloak_admin_username,
        admin_password=keycloak_admin_password,
        udm_url=f"{portal_base_url}/univention/udm/",
        udm_username=admin_username,
        udm_password=admin_password,
        existing_realm="nubus",
        dummy_realm="test",
    )
    ad_hoc_provisioning.setup()
    yield ad_hoc_provisioning

    ad_hoc_provisioning.cleanup()


@pytest.mark.xfail(reason="Keycloak does not support ad-hoc provisioning yet")
@pytest.mark.parametrize(
    "email_verified,temporary_password",
    [
        (True, False),
        (False, False),
        # TODO: Should we test these cases? They require password changes...
        # (True, True),
        # (False, True),
    ],
)
@pytest.mark.login
@pytest.mark.acceptance_environment
def test_adhoc_provisioning(
    email_verified,
    temporary_password,
    navigate_to_login_page,
    setup_ad_hoc_provisioning,
    udm,
    ldap_base_dn,
    faker,
):
    ad_hoc_provisioning = setup_ad_hoc_provisioning
    username = faker.user_name()
    password = faker.password()
    uuid = uuid4()
    uuid_remote = base64.b64encode(uuid.bytes_le).decode("utf-8")
    user_payload = ad_hoc_provisioning._get_test_user_payload(
        username, password, uuid_remote, email_verified=email_verified, temporary_password=temporary_password
    )
    ad_hoc_provisioning.kc_dummy.create_user(user_payload)

    page = navigate_to_login_page
    login_page = LoginPage(page)

    @retrying_slow
    def ad_hoc_login():
        login_page.page.reload()
        expect(login_page.ad_hoc_provisioning_button).to_be_visible(timeout=1000)

    ad_hoc_login()
    login_page.ad_hoc_provisioning_button.click(timeout=1000)
    login_page.login_and_ensure_success(username, password)
    users = udm.get("users/user")
    udm_user = users.get(f"uid=external-oidc-test-{username},cn=users,{ldap_base_dn}")
    assert udm_user.properties["firstname"] == "Test"
    assert udm_user.properties["lastname"] == "User"
    assert udm_user.properties["e-mail"] == [f"{username}@adhoc.test"]
    assert udm_user.properties["primaryGroup"] == f"cn=Domain Users,cn=groups,{ldap_base_dn}"
    assert udm_user.properties["univentionObjectIdentifier"] == str(uuid)
    assert udm_user.properties["univentionSourceIAM"] == "Federation from test"
