# Changelog

## [0.3.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.2.0...v0.3.0) (2024-08-23)


### Features

* Update common-ci to version 1.32.0 ([247e01d](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/247e01d04ebe2bb8112520a1b0158bf0ff4f6cca))


### Bug Fixes

* Timeout of one full second when waiting for the announcement ([8dc7a9e](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/8dc7a9e0c5dd69e4890da93bb469acabcad03490))

## [0.2.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.1.1...v0.2.0) (2024-08-22)


### Features

* Add "udm-rest-api-client" into Python environment ([2d93dff](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/2d93dff6fbaa2499d2bd729d2b1589bee1242357))
* Add fixture "ldap_base_dn" based on the "udm" fixture ([4d110d7](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/4d110d7d86ce7b138efa0de55e57609acddabe9d))
* Add forgot_password_link to LoginPage ([46e4ca5](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/46e4ca5a7f20d934b724efaed10fcfc6de5e70e5))
* Add new fixture "email_domain" ([d36d841](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/d36d841378cd39f82f1cb874525b494824a76268))
* Add new fixtures "user" and "external_email_domain" ([2d51770](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/2d5177094f10390b26462a31f1c2d056a4b70b65))
* Add PasswordForgottenPage ([b096157](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/b0961572f83b2ac17e3331f775f0817265f0831a))
* Add pytest-subtests ([ae6fd45](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/ae6fd45cebff7a25107c16a3fd269822fd223245))
* Always return the newest found email in MaildevApi ([fd13032](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/fd130327b6360d6088987dc095329546b56201fd))
* Assert that the login works after changing the password ([337e73a](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/337e73ae96355af13af3f6452f1c43c8eba5c5a1))
* Assert that the page "Set new password" is shown after requesting the token ([24b367f](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/24b367fd1e94063be316f522fbbe9eb61a820840))
* Change scope of "udm" fixture to session ([a774ce6](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/a774ce665df4823054a744c520069876bdce92bd))
* Change scope of fixture "email_domain" to "session" ([8060c32](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/8060c324e085a17abbd3c90e53458aec3f0738f3))
* Cover scenario "User requests password forgotten link from login page" ([2bb3dca](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/2bb3dcabb0b8992627f1f29d41a4bf0f9297df60))
* Remove bundled UDM Rest API client ([f5ff08a](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/f5ff08a39b5b47311185d05f61bc400cd846e7d8))
* Remove fixture "udm_ldap_base" ([e77624e](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/e77624e9f3d431cbc9fde28152eddc49fa20a94e))
* Split password forgotten test into subtests ([8f64751](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/8f6475190dfade787c5730c9be94e78caa4a8210))

## [0.1.1](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.1.0...v0.1.1) (2024-08-21)


### Bug Fixes

* Add markers to admin invites new user via email test case ([98b9316](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/98b93160360cbe1f85d029db42441ebd238b6c3c))
