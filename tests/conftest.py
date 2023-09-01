def pytest_addoption(parser):
    # Portal tests options
    parser.addoption("--username", default="Administrator",
                     help="Portal login username",
                     )
    parser.addoption("--password", default="univention",
                     help="Portal login password",
                     )
    parser.addoption("--notifications-api-base-url",
                     default="http://localhost:8000/univention/portal/notifications-api/",
                     help="Base URL of the notification API",
                     )
    parser.addoption("--portal-base-url", default="http://localhost:8000",
                     help="Base URL of the univention portal",
                     )
    # BFP tests options
    parser.addoption("--kc-admin-username", default="admin",
                     help="Keycloak admin login username"
                     )
    parser.addoption("--kc-admin-password", default="univention",
                     help="Keycloak admin login password"
                     )
    parser.addoption("--num-device-block", type=int, default=5,
                     help="Number of failed logins for device block"
                     )
    parser.addoption("--num-ip-block", type=int, default=7,
                     help="Number of failed logins for IP block"
                     )
    parser.addoption("--release-duration", type=int, default=60,
                     help="Blocks are released after this many seconds"
                     )
    parser.addoption("--realm", default="master",
                     help="Realm to attempt logins at"
                     )