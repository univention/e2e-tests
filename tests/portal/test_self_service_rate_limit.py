# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import pytest
import requests

from api.maildev import MaildevApi
from e2e.decorators import retrying
from e2e.email.password_reset import PasswordResetEmail
from e2e.ucr import UCR
from e2e.umc import UniventionManagementConsoleDeployment


@pytest.fixture(scope="class")
def set_self_service_rate_limit(ucr_configmap: UCR, umc_deployment: UniventionManagementConsoleDeployment):
    ucr = ucr_configmap
    ucrv = "umc/self-service/passwordreset/limit/total/day"
    rate_limit = "1"

    original = ucr.get(ucrv)

    ucr.set(ucrv, rate_limit)
    umc_deployment.restart_umc()

    yield

    ucr.set(ucrv, original)
    umc_deployment.restart_umc()


@pytest.fixture()
def reset_rate_limit(umc_deployment: UniventionManagementConsoleDeployment):
    umc_deployment.restart_memcached()


@pytest.fixture()
def create_user_email_invite_factory(udm, faker, external_email_domain, user_password):
    created_users = []

    def _run():
        users_user = udm.get("users/user")
        test_user = users_user.new()
        username = f"test-{faker.user_name()}"

        test_user.properties.update(
            {
                "username": username,
                "lastname": faker.last_name(),
                "password": user_password,
                "pwdChangeNextLogin": True,
                "PasswordRecoveryEmail": f"{username}@{external_email_domain}",
            }
        )

        test_user.save()

        created_users.append(test_user)

        return test_user

    yield _run

    for created_user in created_users:
        created_user.reload()
        created_user.delete()


@pytest.mark.development_environment
@pytest.mark.acceptance_environment
@pytest.mark.usefixtures("set_self_service_rate_limit")
class TestSelfServiceRateLimit:
    @pytest.mark.usefixtures("reset_rate_limit")
    def test_cluster_internal_request_bypass_ratelimit(
        self, create_user_email_invite_factory, email_test_api: MaildevApi
    ):
        n_users = 2
        for _ in range(n_users):
            user = create_user_email_invite_factory()
            assert get_password_reset_link_with_token(email_test_api, user.properties["PasswordRecoveryEmail"])

    # email_test_api fixture is merely used here to skip the test if no SMTP server is configured
    @pytest.mark.usefixtures("reset_rate_limit", "email_test_api")
    def test_pw_reset_reqeust_through_frontend_is_ratelimited(self, portal, user):
        username = user.properties["username"]
        pw_reset_url = f"{portal.base_url}univention/command/passwordreset/send_token"

        # the first request should succeed
        resp = password_reset_request(pw_reset_url, username)
        assert resp.status_code == 200

        # the second request should hit the rate-limit
        resp = password_reset_request(pw_reset_url, username)

        assert resp.status_code == 503
        response_body = resp.content.decode()
        expected_msg = "The allowed maximum number of connections to the server has been reached."
        assert expected_msg in response_body, f"{expected_msg=}, {response_body=}"


def password_reset_request(url: str, username: str):
    request_data = {"options": {"username": username, "method": "email"}}
    resp = requests.post(url, json=request_data)

    return resp


def get_password_reset_link_with_token(email_test_api, recovery_email):
    email = retrying(email_test_api.get_one_email)(to=recovery_email)
    password_reset_email = PasswordResetEmail(email)
    return password_reset_email.link_with_token
