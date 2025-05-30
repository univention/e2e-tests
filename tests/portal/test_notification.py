# Like what you see? Join us!
# https://www.univention.com/about-us/careers/vacancies/
#
# Copyright 2001-2023 Univention GmbH
#
# https://www.univention.de/
#
# All rights reserved.
#
# The source code of this program is made available
# under the terms of the GNU Affero General Public License version 3
# (GNU AGPL V3) as published by the Free Software Foundation.
#
# Binary versions of this program provided by Univention to you as
# well as other copyrighted, protected or trademarked materials like
# Logos, graphics, fonts, specific documentations and configurations,
# cryptographic keys etc. are subject to a license agreement between
# you and Univention and not subject to the GNU AGPL V3.
#
# In the case you use this program under the terms of the GNU AGPL V3,
# the program is provided in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License with the Debian GNU/Linux or Univention distribution in file
# /usr/share/common-licenses/AGPL-3; if not, see
# <https://www.gnu.org/licenses/>.

import copy
import time
import uuid
from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin

import pytest
import requests
from url_normalize import url_normalize

from umspages.common.base import expect
from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.home_page.logged_out import HomePageLoggedOut


@pytest.fixture()
def notifications_api_base_url(portal):
    return urljoin(portal.base_url, "/univention/portal/notifications-api/")


@pytest.fixture()
def login_and_clear_old_notifications(navigate_to_home_page_logged_in_as_admin, admin_username, admin_password):
    page = navigate_to_home_page_logged_in_as_admin
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.remove_all_notifications()
    yield page
    # TODO: Clear notifications in another way, e.g. fresh context? We don't
    # know if we are logged in or not and instead of doing "if then else and if
    # not" magic, a clean browser context, login, cleanup would be easier to
    # understand.
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.navigate(admin_username, admin_password)
    home_page_logged_in.remove_all_notifications()


@pytest.fixture()
def notification_json_data():
    unique_id = str(uuid.uuid4())
    json_data = {
        "sourceUid": unique_id,
        "targetUid": unique_id,
        "title": "Test title",
        "details": "Test details",
        "severity": "info",
        "sticky": True,
        "needsConfirmation": True,
        "notificationType": "event",
        "link": {
            "url": "https://test.org",
            "text": "Test link text",
            "target": "test target",
        },
        "data": {},
    }
    return json_data


@pytest.fixture()
def notification_json_data_different_details(notification_json_data):
    json_data = copy.deepcopy(notification_json_data)
    json_data["details"] = "Different details"
    return json_data


@pytest.fixture()
def send_notification_endpoint(notifications_api_base_url):
    return urljoin(notifications_api_base_url, "./v1/notifications/")


# https://git.knut.univention.de/univention/components/univention-portal/-/issues/712
@pytest.mark.xfail()
@pytest.mark.notifications
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_two_notifications(
    login_and_clear_old_notifications,
    send_notification_endpoint,
    notification_json_data,
    notification_json_data_different_details,
):
    page = login_and_clear_old_notifications
    home_page_logged_in = HomePageLoggedIn(page)
    expect(home_page_logged_in.popup_notification_container).to_be_hidden()
    response = requests.post(send_notification_endpoint, json=notification_json_data)
    assert response.ok, f"Got status {response.status_code} while sending notification"
    expect(home_page_logged_in.popup_notification_container).to_be_visible()
    expect(home_page_logged_in.popup_notification_container.notifications).to_have_count(1)
    notification = home_page_logged_in.popup_notification_container.notification(0)
    expect(notification).to_be_visible()

    link = notification.link
    expect(link).to_have_count(1)
    expected_url = notification_json_data["link"]["url"]
    actual_url = link.get_attribute("href")
    assert url_normalize(expected_url) == url_normalize(
        actual_url
    ), f"Wrong link in notification pop up. Expected: {expected_url}, actual: {actual_url}"

    expected_target = notification_json_data["link"]["target"]
    actual_target = link.get_attribute("target")
    assert (
        expected_target == actual_target
    ), f"Wrong link target in notification pop up. Expected: {expected_target}, actual: {actual_target}"
    expected_link_text = notification_json_data["link"]["text"]
    actual_link_text = link.inner_text()
    assert (
        expected_link_text == actual_link_text
    ), f"Wrong link text in notification pop up. Expected: {expected_link_text}, actual: {actual_link_text}"

    expect(notification.title).to_have_text(
        f"{notification_json_data['severity'].capitalize()}: {notification_json_data['title']}",
    )
    expect(notification.details).to_have_text(notification_json_data["details"])

    response = requests.post(send_notification_endpoint, json=notification_json_data_different_details)
    assert response.ok, f"Got status {response.status_code} while sending notification"
    home_page_logged_in.reveal_area(home_page_logged_in.notification_drawer, home_page_logged_in.header.bell_icon)
    expect(home_page_logged_in.notification_drawer.notifications).to_have_count(2)
    first_notification = home_page_logged_in.notification_drawer.notification(0)
    expect(first_notification).to_be_visible()
    expect(first_notification.details).to_have_text(notification_json_data_different_details["details"])
    second_notification = home_page_logged_in.notification_drawer.notification(1)
    expect(second_notification).to_be_visible()
    expect(second_notification.details).to_have_text(notification_json_data["details"])


@pytest.fixture()
def logout_after_clearing_old_notifications(login_and_clear_old_notifications):
    page = login_and_clear_old_notifications
    home_page_logged_out = HomePageLoggedOut(page)
    home_page_logged_out.navigate()
    home_page_logged_out.is_displayed()
    return page


@pytest.mark.notifications
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_notification_expiry_time(
    logout_after_clearing_old_notifications,
    send_notification_endpoint,
    notification_json_data,
    admin_username,
    admin_password,
):
    page = logout_after_clearing_old_notifications

    dt_now = datetime.now(timezone.utc)
    expiry_dt = dt_now + timedelta(seconds=5)
    notification_json_data["expireTime"] = expiry_dt.isoformat()

    response = requests.post(send_notification_endpoint, json=notification_json_data)
    assert response.ok, f"Got status { response.status_code } while sending notification: { response.text }"

    wait = (expiry_dt - dt_now).total_seconds()
    time.sleep(wait + 1)  # +1 for safety
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.navigate(admin_username, admin_password)
    home_page_logged_in.is_displayed()
    expect(home_page_logged_in.popup_notification_container).to_be_hidden()
    home_page_logged_in.reveal_area(home_page_logged_in.notification_drawer, home_page_logged_in.header.bell_icon)
    expect(home_page_logged_in.notification_drawer.no_notifications_heading).to_be_visible()
    expect(home_page_logged_in.notification_drawer.notifications).to_have_count(0)

    notification_json_data["expireTime"] = (datetime.now(timezone.utc) + timedelta(seconds=5)).isoformat()
    response = requests.post(send_notification_endpoint, json=notification_json_data)
    assert response.ok, f"Got status { response.status_code } while sending notification: { response.text }"
    expect(home_page_logged_in.notification_drawer.no_notifications_heading).to_be_hidden()
    expect(home_page_logged_in.notification_drawer.notifications).to_have_count(1)
    expect(home_page_logged_in.notification_drawer.notification(0)).to_be_visible()
