# Changelog

## [0.19.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.18.0...v0.19.0) (2024-12-03)


### Features

* adapt test to new users module defaults ([bc8d918](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/bc8d9186fe1de73a0a2db27a399bbeded89b97fb))

## [0.18.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.17.0...v0.18.0) (2024-11-28)


### Features

* adapt testing-api for ldap server primary service ([c32daf4](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/c32daf4e24707dcf56ce0760f9a4b8c5d0b496b2))
* upgrade testing-api tag ([d1f9eb6](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/d1f9eb684b63767462b9021d38fe576c794c8dde))

## [0.17.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.16.1...v0.17.0) (2024-11-27)


### Features

* Add a generated script "testing-api" to run the API ([88696bc](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/88696bc8a53853ba3d6fcbe81f04c4c3ae60a090))
* Smarter layer caching in testing-api container ([9326232](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/9326232cf967fa0f5723c590a65c6ec0cf6faf42))

## [0.16.1](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.16.0...v0.16.1) (2024-11-14)


### Bug Fixes

* **test-stability:** increase language assertion locator timeout for 5 seconds to 10 seconds ([437fda8](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/437fda89f3aa6096094beba889362edac71e83cc))

## [0.16.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.15.0...v0.16.0) (2024-11-06)


### Features

* adapting test for Nubus selfservice ([de3f5e2](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/de3f5e27cd09fe161540023e73cf19d997780887))
* add E2E test for pwdChangeNextLogin ([bba08bc](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/bba08bc1878f83fe6212d8846265d936875cd2e3))
* add test for UMC tiles ([61e2e8c](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/61e2e8c614ab135175bd22637e3efc8e33223ef4))
* add tests for portal tiles, sidebar and central navigation ([35fa877](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/35fa87735ec3bff5e8639b3359f41ebecb3173d1))
* change default discovery of keycloak url ([f0262ed](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/f0262ed40628ff28d7fa19bd76ac8507fda81766))
* Change language coverage for Tiles and UMC ([2c4dfb2](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/2c4dfb28d037cdb3768a178074c00812120b9171))
* test upload profile picture  in manage profile ([bbd2b74](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/bbd2b74ad03595eb72e06e02b0f4f891d4420908))
* UMC groups ([7892272](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/789227243ce0529796078f170309496c6a8a166d))


### Bug Fixes

* adapt tests to nubus plain ([61f5f00](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/61f5f00ce0414a09675b11b6be20e59406dd458b))

## [0.14.3](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.14.2...v0.14.3) (2024-09-17)


### Bug Fixes

* Increase timeout when waiting for announcements page to be visible ([c88c842](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/c88c842254be072c39f8a910a34440850e2aa8b2))

## [0.14.2](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.14.1...v0.14.2) (2024-09-16)


### Bug Fixes

* Remove matching for German translation in login_page ([d4df213](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/d4df2137ccc16036c5d73d62994a8b09e131beeb))

## [0.14.1](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.14.0...v0.14.1) (2024-09-13)


### Bug Fixes

* Select form inputs via role in ChangePasswordDialogPage ([df6df29](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/df6df29083f7f56487e7283c0a6ebf9c3b2c926b))
* Select password retype box via role ([584b97c](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/584b97c8faad8221482ba95fa7758a6d12448235))

## [0.14.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.13.1...v0.14.0) (2024-09-13)


### Features

* Cover password forgotten via selfservice portal ([ee3552c](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/ee3552c946f76f5d285004c4ef464bd8d6499eb7))

## [0.13.1](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.13.0...v0.13.1) (2024-09-13)


### Bug Fixes

* Remove code which tries to login only if needed from navigate ([f4e7124](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/f4e71241b0e1929debc90310f691c50f2286e460))

## [0.13.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.12.0...v0.13.0) (2024-09-11)


### Features

* Add "tiles" to "PortalPage" ([3d6ee6d](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/3d6ee6d6b4b4f5880f50ca2101d831dbeea91b12))
* Add locator for UMC Tiles headline into the SelfservicePortal ([cc217e7](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/cc217e7876f6fa1b5735248ab0f93a8ff69ff0be))
* Add test to verify that admin does not see UMC tiles in Selfservice portal ([502554f](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/502554f4ae2a48872c81ac3134e4df5db3ef7360))
* Use PortalPage.tiles in HomePageLoggedIn ([a18d71e](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/a18d71ecc2b2747263d78f1a598b28be2972b842))

## [0.12.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.11.0...v0.12.0) (2024-09-11)


### Features

* Add "login_with_retry" to LoginPage ([891c47d](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/891c47de29ce138959be6df19627e9205dcc8722))
* Check selfservice portal for regular user ([a7b310c](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/a7b310cd460def415e3d71b1a773d287fba633f6))
* Remove fixture "navigate_to_selfservice_portal_logged_in" ([15c7c81](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/15c7c813e56191c59e452238a7b30404fcee845d))
* Remove unused fixture "navigate_to_selfservice_portal_logged_out" ([a86da8b](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/a86da8bd3f90b39a700eff6342b163662e0b49ab))
* Simplify the ~navigate~ of the page ~SelfServicePortalLoggedOut~ ([b934026](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/b934026bc7532be093d51f2a22aa954b12a7aeac))
* Split the test regarding the selfservice portal ([f75a600](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/f75a6003fd35ca17f6531d404889957ecd3dc6e8))
* Use "login_with_retry" in SelfservicePortalLoggedIn ([c6713af](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/c6713af3b674955386b01e606fe1ab8decace68c))

## [0.11.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.10.0...v0.11.0) (2024-09-10)


### Features

* Change Pipefile to use the latest version of all dependencies ([71bda60](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/71bda605738825e105246c7df6b94acba3a7ec6c))
* Update lock file to latest version for all dependencies ([a50c5c7](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/a50c5c76fe2c0cf7800258ae54bbcb34fc8ba056))

## [0.10.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.9.0...v0.10.0) (2024-09-09)


### Features

* better failed test summary when tenacity retries are involved ([d6aecc1](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/d6aecc1a6090dc9f02b9fd5e9d991f8952d5d396)), closes [univention/customers/dataport/team-souvap#807](https://git.knut.univention.de/univention/customers/dataport/team-souvap/issues/807)
* wait for the portal-consumer to catch up by polling navigate.json ([56ed4cc](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/56ed4cca897eb813719a10e58f425287f242516c)), closes [univention/customers/dataport/team-souvap#807](https://git.knut.univention.de/univention/customers/dataport/team-souvap/issues/807)


### Bug Fixes

* decrease click timeout because the menu entry will never appear if an outdated portal.json was loaded ([9e84588](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/9e845886f6c36ced4cd638c91d935c4918e0f613)), closes [univention/customers/dataport/team-souvap#807](https://git.knut.univention.de/univention/customers/dataport/team-souvap/issues/807)
* fix code after rebase ([d2bbc34](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/d2bbc3418c54b7bcda5a460911ee548495aed972))
* make discover env script compatible with openDesk again ([4e9b680](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/4e9b68034bde4407cc400ca53459db76f591f665))
* make faker seed unique to every test function instead of one for the whole session ([6e0b870](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/6e0b870625dfac0bd2d86e20d925ee782c6cf637)), closes [univention/customers/dataport/team-souvap#807](https://git.knut.univention.de/univention/customers/dataport/team-souvap/issues/807)
* make the login form response inspection compatible with openDesk deployments in addition to plain nubus deployments ([38a5fcc](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/38a5fcc41fe116fbb7e3fb4939a8e27c88dd4e87)), closes [univention/customers/dataport/team-souvap#807](https://git.knut.univention.de/univention/customers/dataport/team-souvap/issues/807)
* set log level for failed tests ([968e7f0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/968e7f00a344e5a72570e44e079e4ddc9e09175e)), closes [univention/customers/dataport/team-souvap#807](https://git.knut.univention.de/univention/customers/dataport/team-souvap/issues/807)
* Stabilize selfservice tests when run against opendesk with portal-consumer ([a1b9f1e](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/a1b9f1e4027d415680689f3d5d7e2d400bda5c1e)), closes [univention/customers/dataport/team-souvap#807](https://git.knut.univention.de/univention/customers/dataport/team-souvap/issues/807)

## [0.9.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.8.3...v0.9.0) (2024-09-09)


### Features

* Update playwright to version 1.46.0 ([0e6a90f](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/0e6a90f3290db912c4214a522a85c89576319cc8))


### Bug Fixes

* Replace "page.expect_response" with "page.route" ([48aeac2](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/48aeac2d85f3ac0a451acbfe0985d74c9c7d9895))
* Wait until response is finished before looking into the body ([d6d83fc](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/d6d83fcb2bc824ff4708527981afc301256102f1))
* wip - Inspect the response of the login form to ensure it worked ([d5f1cd8](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/d5f1cd885bea4e04d6898529022d736ba11123ea))

## [0.8.3](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.8.2...v0.8.3) (2024-09-06)


### Bug Fixes

* Increase the timeout of the login redirection to 5 seconds ([526c8fe](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/526c8fefddc8f2358a657c731f9e4e2500ac7001))

## [0.8.2](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.8.1...v0.8.2) (2024-09-06)


### Bug Fixes

* Avoid failing if some secrets are missing ([a79b60c](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/a79b60c71295283dd6ea9b8368d1b18f3a9394ea))

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
