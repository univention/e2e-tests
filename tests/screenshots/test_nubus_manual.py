import pytest

from umspages.common.base import expect
from univention.admin.rest.client import UnprocessableEntity

from .conftest import (
    screenshot_path,
    set_viewport_size,
    switch_language,
    viewport_size_for_screenshots_1280_720,
)

# List of files used in Nubus Manual
# [ ] - admin-helpdesk.png
# [x] - computers_computer_advanced.png
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


def create_network_object_default(udm):
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
    except UnprocessableEntity as exc:
        print(exc)


def create_forward_zone(udm):
    dns_module = udm.get("dns/forward_zone")
    dns = dns_module.new()
    dns.properties.update(
        {
            "zone": "example.org",
            "nameserver": ["ns.example.org"],
        }
    )
    try:
        dns.save()
    except UnprocessableEntity as exc:
        print(exc)


DEVICE_SCREENSHOTS = [
    pytest.param("Devices", "devices", None, id="en"),
    pytest.param("Geräte", "devices-de", "Deutsch", id="de"),
]

COMPUTER_LABELS = {
    "de": {
        "tile": "Rechner iFrame",
        "iframe": "Rechner",
        "add": "Hinzufügen",
        "computer_type": "Rechner: macOS client",
        "next": "Weiter",
        "client_name": "Rechnername *",
        "ip_address": "IP-Adresse",
        "dialog": "Neuen Rechner hinzufügen.",
        "advanced": "Erweitert",
        "operating_system": "Betriebssystem",
        "network_settings": "Netzwerk-Einstellungen",
        "description": "Beschreibung",
    },
    "en": {
        "tile": "Computers iFrame",
        "iframe": "Computers",
        "add": "Add",
        "computer_type": "Computer: macOS client",
        "next": "Next",
        "client_name": "Client name *",
        "ip_address": "IP address",
        "dialog": "Add a new computer.",
        "advanced": "Advanced",
        "operating_system": "Operating system",
        "network_settings": "Network settings",
        "description": "Description",
    },
}

COMPUTER_SCREENSHOTS = [
    pytest.param(COMPUTER_LABELS["en"], "", None, id="en"),
    pytest.param(COMPUTER_LABELS["de"], "-de", "Deutsch", id="de"),
]


@pytest.mark.screenshots
@pytest.mark.parametrize("screenshot_page", [viewport_size_for_screenshots_1280_720], indirect=True)
@pytest.mark.parametrize("folder_name,filename,target_language", DEVICE_SCREENSHOTS)
class TestScreenshotUIGroups(object):
    manual_path: str = "nubus-manual"

    def test_devices(
        self,
        navigate_to_home_page_logged_in_as_admin,
        screenshots_output_dir,
        screenshot_page,
        folder_name,
        filename,
        target_language,
    ):
        page = navigate_to_home_page_logged_in_as_admin
        switch_language(page, target_language)
        folder = page.locator(".portal-folder").filter(has_text=folder_name)
        expect(folder).to_be_visible()
        folder.click()

        locator = page.locator('#modal-wrapper--isVisible-1 [data-test="portalFolder"]')
        expect(locator).to_be_visible()
        locator.screenshot(
            path=screenshot_path(screenshots_output_dir, name=filename, path=self.manual_path),
            animations="disabled",
        )


@pytest.mark.screenshots
@pytest.mark.parametrize("screenshot_page", [viewport_size_for_screenshots_1280_720], indirect=True)
@pytest.mark.parametrize("labels,filename_suffix,target_language", COMPUTER_SCREENSHOTS)
class TestScreenshotNubusManualComputersModule(object):
    manual_path: str = "nubus-manual"

    def test_computers_computer(
        self,
        navigate_to_home_page_logged_in_as_admin,
        screenshots_output_dir,
        screenshot_page,
        udm,
        labels,
        filename_suffix,
        target_language,
    ):
        page = navigate_to_home_page_logged_in_as_admin
        switch_language(page, target_language)
        create_network_object_default(udm)

        computers_tile = page.get_by_role("link", name=labels["tile"])
        expect(computers_tile).to_be_visible()
        computers_tile.click()

        frame = page.locator(f'iframe[title="{labels["iframe"]}"]').content_frame
        frame.get_by_role("button", name=labels["add"]).click()
        frame.locator("#widget_umc_widgets_ComboBox_4 span").click()
        frame.get_by_role("option", name=labels["computer_type"]).click()
        frame.get_by_role("button", name=labels["next"], exact=True).click()
        frame.get_by_role("textbox", name=labels["client_name"]).fill("workstation3")
        frame.get_by_role("textbox", name=labels["ip_address"]).fill("10.200.58.10")
        frame.locator("#widget_umc_widgets_ComboBox_6 span").click()
        frame.get_by_role("option", name="default").click()

        dialog = frame.get_by_role("dialog", name=labels["dialog"])
        expect(dialog).to_be_visible()
        dialog.screenshot(
            path=screenshot_path(
                screenshots_output_dir, name=f"computers_computer{filename_suffix}", path=self.manual_path
            )
        )

    def test_computers_computer_advanced(
        self,
        navigate_to_home_page_logged_in_as_admin,
        screenshots_output_dir,
        screenshot_page,
        udm,
        labels,
        filename_suffix,
        target_language,
    ):
        page = navigate_to_home_page_logged_in_as_admin
        switch_language(page, target_language)
        set_viewport_size(page, 1280, 920)
        create_network_object_default(udm)
        create_forward_zone(udm)

        computers_tile = page.get_by_role("link", name=labels["tile"])
        expect(computers_tile).to_be_visible()
        computers_tile.click()

        frame = page.locator(f'iframe[title="{labels["iframe"]}"]').content_frame

        # Navigate to Add computer
        frame.get_by_role("button", name=labels["add"]).click()
        frame.locator("#widget_umc_widgets_ComboBox_4 span").click()
        frame.get_by_role("option", name=labels["computer_type"]).click()
        frame.get_by_role("button", name=labels["next"], exact=True).click()
        # Fill in values in wizard
        frame.get_by_role("textbox", name=labels["client_name"]).fill("workstation3")
        dialog = frame.get_by_role("dialog", name=labels["dialog"])
        expect(dialog).to_be_visible()

        dialog.get_by_role("img").click()
        frame.get_by_role("option", name="default").click()

        # Switch to advanced module view
        frame.get_by_role("button", name=labels["advanced"], exact=True).click()
        frame.get_by_role("textbox", name=labels["operating_system"], exact=True).click()
        frame.get_by_role("textbox", name=labels["operating_system"], exact=True).fill("macOS")
        frame.get_by_role("button", name=labels["network_settings"]).click()

        frame.locator("#widget_umc_modules_udm_ComboBox_2").get_by_role("img").click()
        frame.locator("#widget_umc_modules_udm_ComboBox_2").get_by_role("img").click()
        frame.get_by_role("option", name="example.org").click()
        frame.locator("#umc_widgets_ComboBox_7").click()
        frame.get_by_role("textbox", name=labels["description"]).click()

        page.screenshot(
            path=screenshot_path(
                screenshots_output_dir, name=f"computers_computer_advanced{filename_suffix}", path=self.manual_path
            )
        )
