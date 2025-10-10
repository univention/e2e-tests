# Like what you see? Join us!
# https://www.univention.com/about-us/careers/vacancies/
#
# Copyright 2001-2025 Univention GmbH
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

import pytest

from tests.screenshots.conftest import screenshots_output_dir
from umspages.portal.login_page import LoginPage

from .conftest import (
    screenshot_filename,
    viewport_size_for_screenshots_1280_720,
    viewport_size_for_screenshots_1920_1080,
)

# List of files used in Nubus Manual
# computers_computer_advanced.png
# computers_computer.png
# create-group.png
# create-network.png
# directory-browser-edit.png
# directory-browser.png
# dns-forward-lookup-zone.png
# dns-srv-record.png
# mail_mailinglist.png
# portal-announcements.png
# project-share.png
# self-service.png
# ui-favorites-tab.png
# ui_login.png
# ui_login_sso.png
# ui_user.png
# users_policy_password.png
# users_self-service.png
# users_self-service_profile.png
# users_self-service_registration.png
# users_self-service_verification_email.png
# users_self-service_verification_message.png
# users_self-service_verification.png
# users_user_advanced.png
# users_user.png
# users_usertemplate.png
# users_user_wizard_primary_mail.png


@pytest.mark.screenshots
@pytest.mark.parametrize(
    "screenshot_page", [viewport_size_for_screenshots_1280_720, viewport_size_for_screenshots_1920_1080], indirect=True
)
class TestScreenshotNubusManual(object):
    pass
