# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from contextlib import nullcontext as does_not_raise

import pytest
import requests

pytestmark = [
    pytest.mark.portal,
    pytest.mark.development_environment,
    pytest.mark.acceptance_environment,
]


def test_well_known_favicon_url_works(portal):
    response = requests.get(portal.favicon_well_known_url)
    with does_not_raise():
        response.raise_for_status()
