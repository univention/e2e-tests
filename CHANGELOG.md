# Changelog

## [0.8.1](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.8.0...v0.8.1) (2024-09-05)


### Bug Fixes

* Make support for "RELEASE_NAME" work again ([eb9a0c7](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/eb9a0c7dc70deda7aa06559e9325c53a4aaaac09))

## [0.8.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.7.0...v0.8.0) (2024-09-03)


### Features

* remove default.user and admin for Administrator ([c41869b](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/c41869bc85a8786862e1c98265eac2f5619291fb))

## [0.7.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.6.0...v0.7.0) (2024-08-29)


### Features

* Add decorator "retrying_slow" for special cases ([594ef64](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/594ef64d3b28ae4f11d18bf593553efbdd8fc316))
* Add fixture "user_password" ([5f9045f](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/5f9045f51129e06347978a7848acc9334c12f44d))
* Double timeouts for retrying ([8231bc6](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/8231bc626fb4f1fd630a2e3fdf28ff776d271f02))
* Randomize the faker instance ([b22fefc](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/b22fefc4b31dd246f837d3442d0ee039ebfe4f1c))


### Bug Fixes

* Add minimal delay when filling the set new password form ([5e0cda1](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/5e0cda1f28191184307c0d52ee1306397bc1b5da))
* Avoid double login when clearing notifications ([cd7379b](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/cd7379ba92221cd8d42814de7c65588fb9edab30))
* Further increase the timeout for the login redirect ([468cf73](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/468cf73659af8f56cf74ee1184b52d877a2d8f02))
* HomepageLoggedIn.navigate simplification ([49e7142](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/49e714238dfbb39517fe8cea677083100bd8fbde))
* Increase the timeout for the tiles to become visible ([c188a3b](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/c188a3bf325de8e7413a78e5fa909b5049b26f00))
* Increase timeout for the redirect in login ([2aeb40d](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/2aeb40d6055ecadaeb28e283c4f0fc710c998365))
* Retry until the tiles are visible in HomePageLoggedIn ([e12e05b](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/e12e05b25ef6b895b6bba62ce0090b2c1865bab7))
* Use "retrying_slow" also for the login ([2848158](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/2848158931c4cc29506af3c5e4b7894302c4894a))

## [0.6.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.5.0...v0.6.0) (2024-08-25)


### Features

* **discover:** Be flexible about secret names and values ([641345a](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/641345a811d613a86be9ed07fba98368dc02de69))
* **discover:** Maildev is not always available ([79f2035](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/79f2035ad127bdb767b93bd0f3c4282f5e0387b0))

## [0.5.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.4.0...v0.5.0) (2024-08-23)


### Features

* Skip tests which require Maildev if no URL is configured ([0199319](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/019931967286227d50bf71cfb8bd3e570e47f174))

## [0.4.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.3.0...v0.4.0) (2024-08-23)


### Features

* Allow a custom release name in discover script ([7c2a87f](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/7c2a87fbfd9c74583f04a8873a4ac99aa754685a))

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
