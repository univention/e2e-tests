# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

"""
Kerberos key material across the whole domain.

Checks every entry that carries a `krb5Key`, which includes the accounts
created by the domain bootstrap that no test creates for itself.
"""

import pytest

from e2e.password_hashes import WEAK_KRB5_ENCTYPES, format_enctypes, krb5_enctypes

pytestmark = [
    pytest.mark.password_hashes,
    pytest.mark.development_environment,
    pytest.mark.acceptance_environment,
]


def test_no_weak_kerberos_keys_in_the_domain(ldap_primary):
    entries = ldap_primary.search_entries("(krb5Key=*)", ["krb5Key"])
    assert entries, "No entry carries a krb5Key, so this search proves nothing"

    offenders = {}
    for dn, entry in entries.items():
        weak = krb5_enctypes(entry) & WEAK_KRB5_ENCTYPES
        if weak:
            offenders[dn] = weak

    report = "\n".join(f"  {dn}: {format_enctypes(weak)}" for dn, weak in sorted(offenders.items()))
    assert not offenders, f"{len(offenders)} of {len(entries)} entries carry weak Kerberos keys:\n{report}"
