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

from attrdict import AttrDict


handbook = AttrDict(
    lang='en',
    side_menu=AttrDict(
        MENU_USER_SETTINGS_TEXT='User settings',
        MENU_CHANGE_LENGUAGE_TEXT='Change Language',
        MENU_PRIVACY_BUTTON_TEXT='Privacy statement',
        MENU_LEGAL_BUTTON_TEXT='Legal notice',
        SUBMENU_UPDATE_PASSWORD_TEXT='Update my password',
    ),
    main_page=AttrDict(
        PAGE_HEADER='Sovereign Workplace',
        CATEGORY_1_TITLE='Applications',
        CATEGORY_2_TITLE='Sovereign Workplace',
        CATEGORY_1_LOGIN_WIDGET_TITLE='Login',
        CATEGORY_2_LOGIN_WIDGET_TITLE='Login',
        MENU_LOGIN_BUTTON_TEXT='LOGIN',
    ),
    login_page=AttrDict(
        PAGE_HEADER='UCS',
        LOGIN_FORM_TITLE='Login at null',
        USERNAME_INPUT_LABEL='Username',
        PASSWORD_INPUT_LABEL='Password',
        LOGIN_BUTTON_LABEL='Login',
        MENU_HELP_LABEL='Help',
        MENU_BACK_BUTTON='Back to start site',
    ),
    admin_home_page=AttrDict(
        USER_WIDGET_TITLE='User',
        GROUP_WIDGET_TITLE='Groups',
        MAILBOXES_WIDGET_TITLE='Functional mailboxes',
        RESOURVES_WIDGET_TITLE='Resources',
        ANNOUNCEMENTS_WIDGET_TITLE='Announcements',
        MENU_LOGOUT_TEXT='Logout',
    ),
    user_home_page=AttrDict(
            EMAIL_WIDGET_TITLE='E-Mail',
            CALENDAR_WIDGET_TITLE='Calendar',
            CONTACTS_WIDGET_TITLE='Contacts',
            TASKS_WIDGET_TITLE='Tasks',
            FILES_WIDGET_TITLE='Files',
            ACTIVITY_WIDGET_TITLE='Activity',
            FOLDER_WIDGET_TITLE='Create new files',
            PROJECTS_WIDGET_TITLE='Projects',
            KNOWLEDGE_WIDGET_TITLE='Knowledge',
            COLLABORATION_WIDGET_TITLE='Collaboration',
            VIDEO_WIDGET_TITLE='Ad hoc videoconference',
            MENU_LOGOUT_TEXT='Logout',
        ),
)
