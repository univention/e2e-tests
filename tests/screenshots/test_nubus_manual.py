import pytest

import univention

from .conftest import (
    screenshot_path,
    viewport_size_for_screenshots_1920_1080,
)

# List of files used in Nubus Manual
# [ ] - admin-helpdesk.png
# [ ] - computers_computer_advanced.png
# [x] - computers_computer.png
# [ ] - create-group.png
# [ ] - create-network.png
# [ ] - create_printershare.png
# [ ] - devices_computers_list.png
# [x] - devices.png
# [ ] - directory-browser-edit.png
# [ ] - directory-browser.png
# [ ] - dns-forward-lookup-zone.png
# [ ] - dns-srv-record.png
# [ ] - domain_extended_attribute.png
# [ ] - domain.png
# [ ] - mail_imapfolder.png
# [ ] - mail_mailinglist.png
# [ ] - portal-announcements.png
# [ ] - printer_group.png
# [ ] - project-share.png
# [ ] - self-service.png
# [ ] - ui-favorites-tab.png
# [ ] - ui_login.png
# [ ] - ui_login_sso.png
# [ ] - ui_user.png
# [ ] - users.png
# [ ] - users_policy_password.png
# [ ] - users_self-service.png
# [ ] - users_self-service_profile.png
# [ ] - users_self-service_registration.png
# [ ] - users_self-service_verification_email.png
# [ ] - users_self-service_verification_message.png
# [ ] - users_self-service_verification.png
# [ ] - users_user_advanced.png
# [ ] - users_user.png
# [ ] - users_usertemplate.png
# [ ] - users_user_wizard_primary_mail.png


@pytest.mark.screenshots
@pytest.mark.parametrize("screenshot_page", [viewport_size_for_screenshots_1920_1080], indirect=True)
class TestScreenshotNubusManual(object):
    manual_path: str = "nubus-manual"

    def test_computers_computer(
        self,
        navigate_to_home_page_logged_in_as_admin,
        screenshots_output_dir,
        screenshot_page,
        udm,
    ):
        page = navigate_to_home_page_logged_in_as_admin

        networks_module = udm.get("networks/network")
        network = networks_module.new()
        network.properties.update(
            {
                "name": "default",
                "network": "10.200.58.0",
                "netmask": "24",
                "nextIp": "10.200.58.10",
            }
        )
        try:
            network.save()
        except univention.admin.rest.client.UnprocessableEntity as exc:
            print(exc)

        page.get_by_role("link", name="Computers iFrame").click()
        page.locator('iframe[title="Computers"]').content_frame.get_by_role("button", name="Add").click()
        page.locator('iframe[title="Computers"]').content_frame.locator("#widget_umc_widgets_ComboBox_4 span").click()
        page.locator('iframe[title="Computers"]').content_frame.get_by_role(
            "option", name="Computer: IP client"
        ).click()
        page.locator('iframe[title="Computers"]').content_frame.get_by_role("button", name="Next").click()
        page.locator('iframe[title="Computers"]').content_frame.get_by_role("textbox", name="IP client name *").click()
        page.locator('iframe[title="Computers"]').content_frame.get_by_role("textbox", name="IP client name *").fill(
            "workstation3"
        )
        page.locator('iframe[title="Computers"]').content_frame.get_by_role("textbox", name="IP address").click()
        page.locator('iframe[title="Computers"]').content_frame.get_by_role("textbox", name="IP address").fill(
            "10.200.58.58"
        )
        page.locator('iframe[title="Computers"]').content_frame.locator("#widget_umc_widgets_ComboBox_6 span").click()
        page.locator('iframe[title="Computers"]').content_frame.get_by_role("option", name="default").click()

        locator = page.locator('iframe[title="Computers"]').content_frame.get_by_role(
            "dialog", name="Add a new computer."
        )
        locator.screenshot(
            path=screenshot_path(screenshots_output_dir, name="computers_computer", path=self.manual_path)
        )

    def test_devices(self, navigate_to_home_page_logged_in_as_admin, screenshots_output_dir, screenshot_page):
        page = navigate_to_home_page_logged_in_as_admin
        page.get_by_role("button", name="Devices Folder: 2 Items").click()
        locator = page.locator('#modal-wrapper--isVisible-1 [data-test="portalFolder"]')
        locator.screenshot(
            path=screenshot_path(screenshots_output_dir, name="devices", path=self.manual_path),
            animations="disabled",
        )
