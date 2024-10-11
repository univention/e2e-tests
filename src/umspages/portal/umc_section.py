# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

from ..common.base import BasePagePart, expect


class UMCSection(BasePagePart):
    def __init__(self, page_part_locator):
        super().__init__(page_part_locator)
        self.section_title = self.page_part_locator.locator("h2:has-text('Univention Management Console')")
        self.folders = self.page_part_locator.locator(".portal-folder")

    def get_folder_by_name(self, name):
        return self.folders.filter(has_text=name).last

    def get_folder_content(self, folder):
        return folder.locator(".portal-folder__thumbnails")

    def get_folder_items(self, folder):
        return self.get_folder_content(folder).locator(".portal-folder__thumbnail")

    def get_item_names(self, folder):
        return self.get_folder_content(folder).locator(".portal-tile__name").all_text_contents()

    def assert_folder_contents(self, folder_name, expected_items):
        folder = self.get_folder_by_name(folder_name)
        items = self.get_item_names(folder)
        assert set(items) == set(expected_items), f"Mismatch in {folder_name} folder contents"

    def assert_folder_count(self, expected_count):
        expect(self.folders).to_have_count(expected_count)

    def assert_all_folders_present(self, expected_folders):
        all_folder_names = self.folders.locator(".portal-folder__name").all_text_contents()
        assert set(all_folder_names) == set(expected_folders), "Unexpected folders present"

    def assert_all_items_present(self, expected_items):
        all_item_names = self.page_part_locator.locator(".portal-tile__name").all_text_contents()
        assert set(all_item_names) == set(expected_items), "Unexpected items present"
