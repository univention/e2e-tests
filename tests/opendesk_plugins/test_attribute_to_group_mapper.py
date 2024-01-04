from typing import Sequence, Union

import pytest
from univention.admin.rest.client import UDM, Object, ShallowObject

from udm_helpers.user_args import udm_user_args


def check_group(groups: Sequence[Union[Object, ShallowObject]], name: str) -> bool:
    return any((name in g.dn for g in groups if g.dn))


@pytest.mark.parametrize(
    "attribute_name, group_name",
    [
        ("isOxUser", "managed-by-attribute-Groupware"),
        ("opendeskFileshareEnabled", "managed-by-attribute-Fileshare"),
        ("opendeskProjectmanagementEnabled", "managed-by-attribute-Projectmanagement"),
        (
            "opendeskKnowledgemanagementEnabled",
            "managed-by-attribute-Knowledgemanagement",
        ),
        ("opendeskLivecollaborationEnabled", "managed-by-attribute-Livecollaboration"),
    ],
)
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_udm_rest_attribute_to_group_mapper(udm: UDM, attribute_name, group_name):
    """
    The Atrribute to Group Mapper needs to be installed in both the UDM REST container
    and the UMC Container, thus a normal E2E test would not test the UDM REST implementation.
    """
    settings_ex = udm.get("settings/extended_attribute")
    users_user = udm.get("users/user")
    assert settings_ex
    assert users_user

    assert len(list(settings_ex.search("cn=attribute-to-group-mapper"))) == 1

    test_user: Object = users_user.new()
    user_args = udm_user_args(minimal=True)
    test_user.properties.update(user_args)

    test_user.properties.update(
        {
            "mailPrimaryAddress": f"{test_user.properties['username']}@univention-organization.test",
        }
    )

    test_user.save()

    assert test_user.properties[attribute_name] is True
    assert check_group(test_user.objects["groups"], group_name)

    test_user.properties[attribute_name] = False
    test_user.save()

    test_user.reload()
    test_user.objects["groups"]
    assert not check_group(test_user.objects["groups"], group_name)
