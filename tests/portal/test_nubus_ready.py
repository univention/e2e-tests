# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import logging

from tenacity import before_sleep_log, retry, stop_after_delay, wait_fixed

from e2e.decorators import BetterRetryError
from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.login_page import LoginPage

log = logging.getLogger(__name__)

retrying = retry(
    stop=stop_after_delay(120),
    wait=wait_fixed(5),
    before_sleep=before_sleep_log(log, logging.WARNING),
    retry_error_cls=BetterRetryError,
)


def test_admin_login(page, admin_username, admin_password):
    """Tests that the nubus deployment is ready for testing"""
    login_page = LoginPage(page)

    retrying(login_page.navigate)()
    login_page = LoginPage(page)
    retrying(login_page.login)(admin_username, admin_password)

    home_page_logged_in = HomePageLoggedIn(page)
    retrying(home_page_logged_in.assert_logged_in)()
