def pytest_addoption(parser):
    # Portal tests options
    parser.addoption("--portal-base-url", help="Base URL of the univention portal")
    parser.addoption("--username", help="Portal login username")
    parser.addoption("--password", help="Portal login password")
    parser.addoption("--admin-username", help="Portal admin login username")
    parser.addoption("--admin-password", help="Portal admin login password")
    # BFP tests options
    parser.addoption("--keycloak-base-url", help="Base URL of Keycloak")
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
