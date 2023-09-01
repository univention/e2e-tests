# Portal tests


| Group         | Test                                                            | Location                                          |
|---------------|-----------------------------------------------------------------|---------------------------------------------------|
| General       | User can login to portal                                        | `tests/portal/test_login.py`                      |
|               | User can logout                                                 | `tests/portal/test_logout.py`                     |
|               | User can login to portal using SAML                             | `tests/portal/test_saml_login.py`                 |
|               | User can logout when SAML login was used                        | `tests/portal/test_saml_logout.py`                |
| Notifications | Notification pops up when triggered using the notifications API | `tests/portal/test_two_notification.py`           |
|               | Notification has correct title, detail and link attributes      | `tests/portal/test_two_notifications.py`          |
|               | Two notifications are displayed in the correct order            | `tests/portal/test_two_notifications.py`          |
|               | Notification expiry time is respected                           | `tests/portal/test_notification_expiry_time.py`   |
| Translation   | Logged out user is able to change language                      | `tests/portal/test_i18n.py`                       |
| UMC Tile      | Admin user is able to use the Users tile                        | `tests/portal/test_users_page.py`                 |
| Self-service  | Non-admin user can change password                              | `tests/portal/test_non_admin_can_change_password` |


# Keycloak login brute force protection tests

| Test                                                                                                                    | Source                                      |
|-------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
| Many failed login with browser A; browser blocked                                                                       | `tests/bfp/test_block::test_device_block`   |
| Browser A block is released after a minute                                                                              | `tests/bfp/test_block::test_device_block`   |
| Browser A blocked, but browser B can login                                                                              | `tests/bfp/test_block::test_device_block`   |
| Many failed logins with browser A and IP X; browser A blocked. more failed logins with browser B and IP X; IP X blocked | `tests/bfp/test_block::test_ip_block`       |
| IP X block is released after a minute                                                                                   | `tests/bfp/test_block::test_ip_block`       |
| IP X blocked, but IP Y can login                                                                                        | `tests/bfp/test_block::test_ip_block`       |
| OIDC API block for IP address                                                                                           | `tests/bfp/test_block::test_api_ip_block`   |