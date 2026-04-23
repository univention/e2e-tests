# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH

"""
Verify that the udm-rest-api license-cache CronJob updates ``used.user``
on ``/univention/udm/license/`` after new users are created.
"""

import pytest

from udm_helpers.user_args import udm_user_args
from univention.admin.rest.client import NotFound

NUM_USERS = 3


@pytest.fixture
def create_users(udm, email_domain):
    users_module = udm.get("users/user")
    created = []

    def _create(count):
        for _ in range(count):
            args = udm_user_args()
            args["username"] = f"test-license-{args['username']}"
            args["mailPrimaryAddress"] = f"{args['username']}@{email_domain}"
            user = users_module.new()
            user.properties.update(args)
            user.save()
            created.append(user)
        return created

    yield _create

    for user in created:
        try:
            user.reload()
            user.delete()
        except NotFound:
            pass


def _read_license_used_user(udm) -> int:
    license_data = udm.client.resolve_relation(udm.entry, "udm:license")
    return license_data["used"]["user"]


def _refresh_license_cache(k8s, cronjob_name, job_name):
    k8s.trigger_cronjob_as_job(cronjob_name, job_name)
    try:
        k8s.wait_for_job(job_name, timeout=300)
    finally:
        k8s.delete_job(job_name)


@pytest.mark.license_cache
@pytest.mark.acceptance_environment
def test_license_cache_cronjob_reflects_new_users(
    k8s,
    release_name,
    udm,
    faker,
    create_users,
    wait_for_ldap_secondaries_to_catch_up,
):
    cronjob_name = f"{release_name}-udm-rest-api-license-cache"

    def job_name():
        return f"license-cache-e2e-{faker.slug()}"[:63]

    # Refresh the cache to ensure the baseline reflects the current LDAP state.
    # A prior test run may have left a stale value behind.
    _refresh_license_cache(k8s, cronjob_name, job_name())
    baseline = _read_license_used_user(udm)

    create_users(NUM_USERS)
    wait_for_ldap_secondaries_to_catch_up()

    _refresh_license_cache(k8s, cronjob_name, job_name())
    after = _read_license_used_user(udm)

    assert after - baseline == NUM_USERS, (
        f"Expected used.user to increase by {NUM_USERS} (baseline={baseline}, observed={after})"
    )
