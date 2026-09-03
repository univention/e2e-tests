# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

"""
Inspection of the password hashes on an LDAP user object.
Checking that **only** the expected password hash types / password algorithms
are used in the default configuration.
"""

from typing import TYPE_CHECKING

from pyasn1.codec.der.decoder import decode

if TYPE_CHECKING:
    from e2e.ldap import LdapServer
    from e2e.types import LdapDn

PASSWORD_HASH_ATTRIBUTES = [
    "krb5Key",
    "krb5KeyVersionNumber",
    "userPassword",
    "sambaNTPassword",
]

KRB5_ENCTYPE_NAMES = {
    1: "des-cbc-crc",
    2: "des-cbc-md4",
    3: "des-cbc-md5",
    5: "des3-cbc-md5",
    7: "old-des3-cbc-sha1",
    16: "des3-cbc-sha1",
    17: "aes128-cts-hmac-sha1-96",
    18: "aes256-cts-hmac-sha1-96",
    19: "aes128-cts-hmac-sha256-128",
    20: "aes256-cts-hmac-sha384-192",
    23: "arcfour-hmac-md5",
    24: "arcfour-hmac-md5-56",
    25: "camellia128-cts-cmac",
    26: "camellia256-cts-cmac",
}

"""Single DES, 3DES and RC4."""
WEAK_KRB5_ENCTYPES = frozenset({1, 2, 3, 5, 7, 16, 23, 24})

EXPECTED_KRB5_ENCTYPES = frozenset({17, 18, 19, 20})

EXPECTED_USERPASSWORD_SCHEME = "{BCRYPT}"

EXPECTED_SAMBA_NT_PASSWORD = False


def krb5_enctypes(entry: dict[str, list[bytes]]) -> set[int]:
    return {krb5_key_enctype(value) for value in entry.get("krb5key", [])}


def krb5_key_version_number(entry: dict[str, list[bytes]]) -> int:
    return int(entry["krb5keyversionnumber"][0])


def userpassword_scheme(entry: dict[str, list[bytes]]) -> str:
    value = entry["userpassword"][0]
    if not value.startswith(b"{") or b"}" not in value:
        raise ValueError(f"userPassword carries no scheme prefix: {value[:16]!r}")
    return value[: value.index(b"}") + 1].decode()


def format_enctypes(enctypes: set[int]) -> str:
    return ", ".join(f"{number} ({KRB5_ENCTYPE_NAMES.get(number, 'unknown')})" for number in sorted(enctypes))


def read_password_hashes(ldap_server: "LdapServer", dn: "LdapDn") -> dict[str, list[bytes]]:
    """Reads from the primary, so no replication wait is needed."""
    return ldap_server.get_entry(dn, PASSWORD_HASH_ATTRIBUTES)


def assert_password_hashes(entry: dict[str, list[bytes]], dn: "LdapDn", key_version_number: int) -> None:
    enctypes = krb5_enctypes(entry)

    weak = enctypes & WEAK_KRB5_ENCTYPES
    assert not weak, f"{dn} carries weak Kerberos keys: {format_enctypes(weak)}"

    assert enctypes == EXPECTED_KRB5_ENCTYPES, (
        f"{dn} carries Kerberos keys for {format_enctypes(enctypes)}, "
        f"expected {format_enctypes(set(EXPECTED_KRB5_ENCTYPES))}"
    )

    assert userpassword_scheme(entry) == EXPECTED_USERPASSWORD_SCHEME, (
        f"{dn} has a userPassword hashed as {userpassword_scheme(entry)}, expected {EXPECTED_USERPASSWORD_SCHEME}"
    )

    assert ("sambantpassword" in entry) == EXPECTED_SAMBA_NT_PASSWORD, (
        f"{dn} has a sambaNTPassword while password/samba/nthash is expected to be false"
    )

    assert krb5_key_version_number(entry) == key_version_number, (
        f"{dn} is at krb5KeyVersionNumber {krb5_key_version_number(entry)}, expected {key_version_number}"
    )


def krb5_key_enctype(value: bytes) -> int:
    """
    The enctype of one raw `krb5Key`, a DER encoded Heimdal `Key`:

        Key ::= SEQUENCE { mkvno [0] INTEGER OPTIONAL, key [1] EncryptionKey, salt [2] Salt OPTIONAL }
        EncryptionKey ::= SEQUENCE { keytype [0] INTEGER, keyvalue [1] OCTET STRING }

    `mkvno` and the salt type are integers in a `[0]` tag too, so fields are
    selected by tag and never by position.
    """
    key, _ = decode(value)
    encryption_key = _tagged(key, 1, "Key.key")
    return int(_tagged(encryption_key, 0, "EncryptionKey.keytype"))


def _tagged(sequence, tag_id: int, description: str):
    # decode() runs without a schema, so components are generic but keep their tags.
    for position in range(len(sequence)):
        component = sequence.getComponentByPosition(position)
        if component.tagSet[-1].tagId == tag_id:
            return component
    raise ValueError(f"No [{tag_id}] field ({description}) in {sequence.prettyPrint()}")
