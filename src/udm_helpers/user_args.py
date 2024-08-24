# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import random
from datetime import date, datetime, timedelta
from typing import Optional

from faker import Faker

COUNTRY_CODES = (
    "AT",
    "BE",
    "BG",
    "HR",
    "CY",
    "CZ",
    "DK",
    "EE",
    "FI",
    "FR",
    "DE",
    "GR",
    "HU",
    "IE",
    "IT",
    "LV",
    "LT",
    "LU",
    "MT",
    "NL",
    "PL",
    "PT",
    "RO",
    "SK",
    "SI",
    "ES",
    "SE",
)

fake = Faker()


def random_date(start_date: Optional[date] = None, end_date: Optional[date] = None) -> date:
    end_date = end_date or datetime.now().date()
    start_date = start_date or end_date - timedelta(365 * 20)

    return start_date + (end_date - start_date) * random.random()


def udm_user_args(minimal=True, suffix=""):
    _username = fake.user_name() + suffix
    result = {
        "firstname": f"{fake.pystr()}{suffix}",
        "lastname": f"{fake.pystr()}{suffix}",
        "username": _username,
        "displayName": _username,
        "password": fake.pystr(),
        # 'mailHomeServer': f"{ucr['hostname']}.{ucr['domainname']}",
        # 'mailPrimaryAddress': f"{_username}@{ucr['domainname']}",
    }
    if minimal:
        return result

    result.update(
        {
            "birthday": random_date().strftime("%Y-%m-%d"),
            "city": fake.pystr(),
            "country": random.choice(COUNTRY_CODES),
            "description": fake.pystr(),
            "employeeNumber": f"{3 * fake.pyint()}",
            "employeeType": fake.pystr(),
            "organisation": fake.pystr(),
            "postcode": f"{3 * fake.pyint()}",
            "street": fake.pystr(),
            "title": fake.pystr(),
        }
    )

    result.update(
        {
            "roomNumber": [
                f"{3 * fake.pyint()}",
                f"{3 * fake.pyint()}",
            ],
            "departmentNumber": [
                fake.pystr(),
                fake.pystr(),
            ],
            "homePostalAddress": [
                {
                    "street": fake.pystr(),
                    "zipcode": f"{5 * fake.pyint()}",
                    "city": fake.pystr(),
                    fake.pystr(): fake.pystr(),
                },
            ],
            "homeTelephoneNumber": [fake.pystr(), fake.pystr()],
            # 'mailAlternativeAddress': [
            #     f"{uts.random_username()}@{ucr['domainname']}",
            #     f"{uts.random_username()}@{ucr['domainname']}"
            # ],
            "mobileTelephoneNumber": [fake.pystr(), fake.pystr()],
            "pagerTelephoneNumber": [fake.pystr(), fake.pystr()],
            "phone": [f"{12 * fake.pyint()}", f"{12 * fake.pyint()}"],
            # 'secretary': [
            #     f"uid=Administrator,cn=users,{ucr['ldap/base']}",
            #     f"uid=Guest,cn=users,{ucr['ldap/base']}"
            # ],
            "e-mail": [
                f"{fake.user_name()}@{fake.user_name()}",
                f"{fake.user_name()}@{fake.user_name()}",
            ],
        }
    )

    return result
