# Changelog

## [0.58.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.57.1...v0.58.0) (2025-11-25)


### Features

* test Keycloak Infinispan functionality ([b1ba95c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/b1ba95c1506cb483fde62e6e22b434578e69232b)), closes [univention/dev/internal/team-nubus#1374](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1374)

## [0.57.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.57.0...v0.57.1) (2025-11-17)


### Bug Fixes

* use normalized URLs on the adhoc setup ([dbd9277](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/dbd9277865a4f5e88a9abf7914356f0ee65097f4)), closes [univention/dev/internal/dev-issues/dev-incidents#186](https://git.knut.univention.de/univention/dev/internal/dev-issues/dev-incidents/issues/186)

## [0.57.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.56.1...v0.57.0) (2025-11-03)


### Features

* add close modal dialogs on automatic logout test ([45be64f](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/45be64fa81e1310fac9e85c30ec58ff7ffda3c6a)), closes [univention/dev/internal/team-nubus#1443](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1443)

## [0.56.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.56.0...v0.56.1) (2025-10-17)


### Bug Fixes

* search for portal main container by different names to make testing more robust ([388f514](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/388f514a8ee09dfeaf46b684ad3e4b5d9972454a)), closes [univention/dev/internal/team-nubus#1441](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1441) [univention/dev/internal/team-nubus#1441](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1441) [univention/dev/internal/team-nubus#1398](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1398)
* use new keymapping for admin password in changed keycloak secrets ([ff2140b](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/ff2140b53e01c909f86f75b4faef42c45c3f7e4d)), closes [univention/dev/internal/team-nubus#1398](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1398)

## [0.56.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.55.0...v0.56.0) (2025-10-13)


### Features

* adapt central navigation test to OIDC ([3601b01](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/3601b01a020e61ab53abc155e4ef6d5597a3e03e)), closes [univention/dev/internal/team-nubus#1442](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1442)
* disable saml login tile and endpoints by default tests ([1ae0013](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/1ae0013730259a4fe03c9f7352907f0b4eac2b16)), closes [univention/dev/internal/team-nubus#1442](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1442)


### Bug Fixes

* adapt portal layout to OIDC ([1f6da13](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/1f6da13f2ecea630578592d2737ad1eea554f7b6)), closes [univention/dev/internal/team-nubus#1442](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1442)

## [0.55.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.54.0...v0.55.0) (2025-10-06)


### Features

* add automatic logout refresh test ([4ad537c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/4ad537cf5d15fdbc8c05dbd69830ed77956b5b03)), closes [univention/dev/internal/team-nubus#1439](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1439)

## [0.54.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.53.0...v0.54.0) (2025-09-22)


### Features

* use LDAP/Keycloak credentials from existing secrets if running with external dependencies ([edaedf2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/edaedf20ecf76697a539da0056dd460165e89499)), closes [univention/dev/internal/team-nubus#1395](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1395)

## [0.53.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.52.2...v0.53.0) (2025-09-18)


### Features

* migrate to OIDC login by default, keep SAML as option ([da2b562](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/da2b562ebde2f04ca0ccba549f0b8140c01769b4)), closes [univention/dev/internal/team-nubus#1435](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1435)


### Bug Fixes

* Do not capture status code from the final chain of redirections ([263980a](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/263980a815695146583c1fb00e63471761a3a5b8)), closes [univention/dev/internal/team-nubus#1435](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1435)
* login tile selector ([62aedbc](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/62aedbc0aa7600809457397c0e98abfd2b7518e4)), closes [univention/dev/internal/team-nubus#1435](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1435)
* portal layout tests to expect SAML login instead of SSO ([9b3d40c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/9b3d40c7ef0e5e851f3994d7453475f244d97a2f)), closes [univention/dev/internal/team-nubus#1435](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1435)

## [0.52.2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.52.1...v0.52.2) (2025-09-16)


### Bug Fixes

* **deps:** Update dependency univention/dev/nubus-for-k8s/common-ci to v1.44.7 ([1baa6cd](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/1baa6cdff27bac1beb427e2113f220daa1660440)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/issues/0)

## [0.52.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.52.0...v0.52.1) (2025-09-16)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.3-build.20250911 ([9132fdf](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/9132fdf23662264bce265a532f245be974bbe7a1)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/issues/0)

## [0.52.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.51.5...v0.52.0) (2025-09-12)


### Features

* Add tests for UDM basic and oidc auth ([9210215](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/92102152f3662c661b75911dde9200134463f89b)), closes [univention/dev/internal/dev-issues/dev-incidents#138](https://git.knut.univention.de/univention/dev/internal/dev-issues/dev-incidents/issues/138)

## [0.51.5](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.51.4...v0.51.5) (2025-09-12)


### Bug Fixes

* Add central navigation entries to the portal UDM object for tests that need it ([f2ca738](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/f2ca738780447f17f3327ce6550692a7d60d5260)), closes [univention/dev/internal/team-nubus#1416](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1416)
* Replace / Remove wait_for_portal_sync usage because it no longer works after central navigation changes ([4a36e48](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/4a36e4841dadcf3d859047944b04f9672834c6b9)), closes [univention/dev/internal/team-nubus#1416](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1416)

## [0.51.4](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.51.3...v0.51.4) (2025-09-12)


### Bug Fixes

* **deps:** Update dependency univention/dev/nubus-for-k8s/common-ci to v1.44.6 ([5307a3a](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/5307a3a93ceae9de64b1c3641175e401dee3c70a)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/issues/0)

## [0.51.3](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.51.2...v0.51.3) (2025-09-12)


### Bug Fixes

* **deps:** Update mcr.microsoft.com/playwright/python Docker tag to v1.55.0 ([c2fc368](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/c2fc368daa2ac204fa69eea33ff3cc2412d550cd)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/issues/0)

## [0.51.2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.51.1...v0.51.2) (2025-09-11)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.3-build.20250909 ([62bc1a0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/62bc1a0f2726e2a9dadd0c2d43ad19a94cb0a238)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/issues/0)

## [0.51.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.51.0...v0.51.1) (2025-09-10)


### Bug Fixes

* reload page on retry for test_user_can_access_2fa_selfservice ([5d8e507](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/5d8e50706a59fb80d302c9ce67fcee8240ac3457)), closes [univention/dev/internal/team-nubus#1420](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1420)
* simply default value for counting test failures ([8f365ec](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/8f365ec1236efa7a05f0399e3121d04a78499e7e)), closes [univention/dev/internal/team-nubus#1410](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1410)

## [0.51.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.50.0...v0.51.0) (2025-09-08)


### Features

* **ready-check:** Administrator login check with long retry timeouts to let the environment get ready ([749ac4c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/749ac4cbc20be87b5bfaf987330e3307bff73e60)), closes [univention/dev/internal/team-nubus#1409](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1409)
* **ready-check:** Initial version of a ready check script ([aa2c004](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/aa2c004ffbcea8014f23f1fa552be07b0c69b654)), closes [univention/dev/internal/team-nubus#1409](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1409)


### Bug Fixes

* Introduce docker-compose service to make e2e tests more easily executable ([c485006](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/c485006efe9585745a5f7591587f49351facc758)), closes [univention/dev/internal/team-nubus#1409](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1409)
* **ready-check:** Better configuration options and validation ([88c588e](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/88c588e5692fce28e353f6d492a5ce52fdafd6f3)), closes [univention/dev/internal/team-nubus#1409](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1409)
* **ready-check:** Better log output and code refactoring ([c2bb873](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/c2bb873fe5899e233cab834037c3e820a16efb31)), closes [univention/dev/internal/team-nubus#1409](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1409)
* **ready-check:** Check container status in addition to pod status ([8b94a87](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/8b94a87cb731de2a4bde3374012a657c6608d9a2)), closes [univention/dev/internal/team-nubus#1409](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1409)
* **ready-check:** Make deployment ready check executable ([72cb6f1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/72cb6f12f79a9e93ed9bc6d225f8fc0f5dc4dadd)), closes [univention/dev/internal/team-nubus#1409](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1409)
* **ready-check:** remove pod from status dict on delete event ([e4a5e6e](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/e4a5e6ecaa004113214e16bf1d07bd66864352c5)), closes [univention/dev/internal/team-nubus#1409](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1409)

## [0.50.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.49.6...v0.50.0) (2025-09-08)


### Features

* add pytest retry wrapper with backup/restore of artifacts ([62cfc8e](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/62cfc8eee39cef99ac7c543ac30aad7f3657dab7)), closes [univention/dev/internal/team-nubus#1410](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1410)


### Bug Fixes

* typo in test name ([949047b](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/949047b6c0d13049461b9d31a0b27a8efa2a3d6e)), closes [univention/dev/internal/team-nubus#1410](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1410)

## [0.49.6](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.49.5...v0.49.6) (2025-09-06)


### Bug Fixes

* **deps:** Update dependency univention/dev/nubus-for-k8s/common-ci to v1.44.4 ([bd9170c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/bd9170cc1e4268f961db7e7a51c29610f992067c)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/issues/0)

## [0.49.5](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.49.4...v0.49.5) (2025-09-05)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.2-build.20250904 ([554fcf2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/554fcf29d8b0816f2ee0b633cf425c84344b70ae)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/issues/0)

## [0.49.4](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.49.3...v0.49.4) (2025-09-05)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.2-build.20250828 ([9873c82](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/9873c82b79683b7c2babc1d1145b2c806ec06b8c)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/issues/0)

## [0.49.3](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.49.2...v0.49.3) (2025-08-28)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.2-build.20250821 ([f047216](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/f047216cd32e9ab8fd24664f694a371113cce0e1)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/issues/0)

## [0.49.2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.49.1...v0.49.2) (2025-08-28)


### Bug Fixes

* **deps:** Update dependency univention/dev/nubus-for-k8s/common-ci to v1.44.2 ([10699a0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/10699a07d0bc76d5cd7f6804282703d84547eeaa)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/issues/0)

## [0.49.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.49.0...v0.49.1) (2025-08-28)


### Bug Fixes

* **deps:** Update dependency requests to v2.32.5 ([d48509c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/d48509c59a64006d5f5508ae35f71b8b641d1997)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/issues/0)
* **deps:** Update dependency tests/requests to v2.32.5 ([a14c2dd](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/a14c2ddf92c53cc73fccb95194135b73213c73ba)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/issues/0)

## [0.49.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.48.3...v0.49.0) (2025-08-22)


### Features

* **left_sidebar:** toggle testing: add dummy test marked as feature toggle ([31d8369](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/31d83691b7447a14dba55fc1fa1cd39c4da3dee7)), closes [univention/dev/internal/team-nubus#1122](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1122)
* **left-sidebar:** add test for left sidebar accessibility ([c5957b7](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/c5957b7eca53c9e77b38336156b53fd8fa59a977)), closes [univention/dev/internal/team-nubus#1122](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1122)

## [0.48.3](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.48.2...v0.48.3) (2025-08-20)


### Bug Fixes

* **deps:** Update dependency univention/dev/nubus-for-k8s/common-ci to v1.44.1 ([b54886d](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/b54886daa4514bf00a46bf5c864a5318dbab6d49)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/issues/0)

## [0.48.2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.48.1...v0.48.2) (2025-08-19)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.2-build.20250814 ([966b967](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/966b9674017343350e2ff4601c87d2d49e540b6b)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/issues/0)

## [0.48.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.48.0...v0.48.1) (2025-08-19)


### Bug Fixes

* **deps:** Pin gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to 7cf8594 ([afcce10](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/afcce10e01534fcd473a0c06f3f3b23bda1ac559)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/issues/0)

## [0.48.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.47.1...v0.48.0) (2025-08-12)


### Features

* tests for configurable central navigation ([0ccb4e2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/0ccb4e212e5af7551a89fc98ef2fbe938c3fdf9a)), closes [univention/dev/internal/team-nubus#1301](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1301)

## [0.47.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.47.0...v0.47.1) (2025-07-21)


### Bug Fixes

* use first button locator when checking for interactive elements ([c2aca8c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/c2aca8cbd8a4250aac58d521d848d4bc4bca33c1)), closes [univention/dev/internal/team-nubus#1217](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1217)

## [0.47.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.46.0...v0.47.0) (2025-07-18)


### Features

* **2fa:** test admin/user accesses self-service, admin accesses admin page ([8fc05b1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/8fc05b1fb198961d95780e39fc8e1cb56c7d00b3)), closes [univention/dev/internal/team-nubus#1217](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1217)

## [0.46.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.45.0...v0.46.0) (2025-07-17)


### Features

* update ucs-base to 5.2.2-build.20250714 ([21863df](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/21863df1ccf185e04d54b1efd473a8c5fcb24fc5)), closes [univention/dev/internal/team-nubus#1320](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1320)

## [0.45.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.44.1...v0.45.0) (2025-07-11)


### Features

* add SCIM API end-to-end test script ([527cc50](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/527cc5026f14684c1edc448d3144f3903ecfff4e)), closes [univention/dev/internal/team-nubus#1113](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1113)

## [0.44.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.44.0...v0.44.1) (2025-06-30)


### Bug Fixes

* skip both selfservice rate limit tests if email test api is missing ([d05b6bc](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/d05b6bcf7de7ad2e376489a5ebc0e8253b80db59)), closes [univention/dev/internal/team-nubus#1311](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1311)

## [0.44.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.43.2...v0.44.0) (2025-06-27)


### Features

* Adjust discovery of ldap credentials to new secret structure ([f0e477a](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/f0e477a84e6e200bc14af7268ae12e31865d6f89)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* Adjust ldap secret name to use "-admin" suffix ([a292faf](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/a292faf4d62631124ec81c297c3f77b38ea25cf2)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* Adjust timeout to wait for the portal consumer to 120 seconds ([5a0d77a](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/5a0d77ab789d28741dd406916ce2dc77f9066664)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)

## [0.43.2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.43.1...v0.43.2) (2025-06-21)


### Bug Fixes

* trigger release ([0057224](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/00572247903c8f4756a47bcd1e3bdbc5c0f4f9a5)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/issues/0)

## [0.43.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.43.0...v0.43.1) (2025-06-18)


### Bug Fixes

* bump umc-base-image version ([4890799](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/4890799ae6adf8feb354e23031f5ad79165c0123)), closes [univention/dev/internal/team-nubus#1263](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1263)

## [0.43.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.42.0...v0.43.0) (2025-06-10)


### Features

* Add 2FA Helpdesk tiles into the expected portal layout ([b158c55](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/b158c55656f8a1836837972eb3012fa934076daa)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* Add property "central_navigation_url" into PortalDeployment ([d5f1a8a](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/d5f1a8a7aaf6f922997a0543b508b5ca0aac6b04)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* add tests for self-service rate-limit ([60065b2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/60065b2ddb4c5625a47a1da6f1a80a76984ba64f)), closes [univention/dev/internal/team-nubus#1220](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1220)
* Allow to discover central navigation secret with old volume name ([d0c6c12](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/d0c6c12c30ab6da5b72b1c104380d883952df361)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* allow usage of external minio deployment ([db32321](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/db32321bb3da922b2cabb6c56cd1bc3720f3689c)), closes [univention/dev/internal/team-nubus#950](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/950)
* Discover central navigation secret from cluster in portal fixture ([b5116c7](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/b5116c7ecec08075e435ba5326246c3911e43f6e)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* Remove fixture "navigation_api_url", use PortalDeployment.central_navigation_url instead ([ac6e0f4](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/ac6e0f43b2ffa52adb1cc46e3be3f95d2e4cffd5)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* test univentionObjectIdentifier in user and admin groups ([137ade5](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/137ade5df274b4f6b8c9a5308c158b735792eeb3)), closes [univention/dev/internal/team-nubus#1220](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1220)


### Bug Fixes

* **portal-tests:** Increase ensure_user_exists timeout to 30s ([cb6e34d](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/cb6e34d0c6b93aa76503e6dd79a8b47829786905)), closes [univention/dev/internal/team-nubus#1223](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1223)
* **testing-api:** Set correct ingress TLS settings ([611e93f](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/611e93f7a3a93a1db7cac07c4376c4753a368498)), closes [univention/dev/internal/team-nubus#1223](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1223)
* **testing-api:** Use correct deploy namespace when getting TLS secret from protal-server ([ba64bed](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/ba64bed1d6e3a44e7c8a2adf416c325f87ff4039)), closes [univention/dev/internal/team-nubus#1223](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1223)

## [0.42.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.41.0...v0.42.0) (2025-05-27)


### Features

* Ensure that the univentionObjectIdentifier set for users created via the UMC ([ce826ed](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/ce826ed7f9eb1b298b958c78e48aaf3a99a64372)), closes [univention/dev/internal/team-nubus#1143](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1143)
* **udm:** Add UniventionObjectIdentifier tests ([8b7c200](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/8b7c2001fec67dc5400a1dc148e32e18191aeb4d)), closes [univention/dev/internal/team-nubus#1143](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1143)
* **udm:** Test the openapi.json generation ([f8d93bb](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/f8d93bb2a3bcc68cb65ec2501d3d663730f432f1)), closes [univention/dev/internal/team-nubus#1143](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1143)


### Bug Fixes

* pin base image to try and avoid caching problems ([1760901](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/1760901cf61b03d7980e2ee93b64878a72348692))
* The result_data may include the autogenerated univentionObjectIdentifier which is not part of the request ([55f0b6c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/55f0b6cae08f78ae27c7d16f2b045f30c635d2ed))
* update playwright base image to try and solve caching problems ([a551ed7](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/a551ed760a22fe298b8a3fa10de6db16855abf72))

## [0.41.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.40.0...v0.41.0) (2025-05-21)


### Features

* test no portal icons are missing (i.e. no question mark icons exist) ([66ad10d](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/66ad10d5344b4d3188ce96a5175cfd875d61f72f)), closes [univention/dev/internal/team-nubus#1182](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1182)

## [0.40.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.39.2...v0.40.0) (2025-05-19)


### Features

* add playwright tests for the corner/quick links feature ([88159b7](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/88159b7909c1f9f24ef28c5feb57b01293014e3c)), closes [univention/dev/internal/team-nubus#1177](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1177)

## [0.39.2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.39.1...v0.39.2) (2025-05-16)


### Bug Fixes

* wait for user entry in s3 instead of original portal sync ([9f28068](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/9f280689267ff475ebaa463420889f92248663ff))

## [0.39.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.39.0...v0.39.1) (2025-05-12)


### Bug Fixes

* **autodiscovery:** Add override for the udm_base_url and only evaluate the kubernetes manifests if no override is specified ([a78cf89](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/a78cf8927653494ed4fb71e36f5f625f1b5d147f)), closes [univention/dev/internal/team-nubus#1143](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1143)
* **autodiscovery:** consolidate configuration from env and cli to cli arguments ([4461f05](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/4461f05a4c982f980587e62c8486842655a66962)), closes [univention/dev/internal/team-nubus#1143](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1143)
* **autodiscovery:** Dont't try to discover the keycloak url if it's overwritten via cli ([cadb6a4](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/cadb6a443fb0b055ba159181e95043c733107045)), closes [univention/dev/internal/team-nubus#930](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/930)

## [0.39.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/compare/v0.38.0...v0.39.0) (2025-05-11)


### Features

* move and upgrade ucs-base-image to 0.17.3-build-2025-05-11 ([f0fde96](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/f0fde9667829ccc87ef27f56f150187c0c49be9d))


### Bug Fixes

* move addlicense pre-commit hook ([5d7999a](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/5d7999ada75cbdbf62fbc398dbb82fab08fcc630))
* update common-ci to main ([4208923](https://git.knut.univention.de/univention/dev/nubus-for-k8s/e2e-tests/commit/4208923b486a3daf6e7268d7a6d2f5df99fcf3e5))

## [0.38.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.37.0...v0.38.0) (2025-05-08)


### Features

* Add response body into the error message of notifications tests ([df7933d](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/df7933d2025fefa348005d2f095b1c815e650a09))

## [0.37.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.36.0...v0.37.0) (2025-04-29)


### Features

* Bump ucs-base-image version ([5c8e19f](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/5c8e19f09a81dea5086db1cc06f13bef5c46f7df)), closes [univention/dev/internal/team-nubus#1155](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1155)

## [0.36.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.35.0...v0.36.0) (2025-04-29)


### Features

* **testing-api:** Remove docker.io dependencies ([344b9a2](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/344b9a2d7f8f4e5a305f372e2518cd9b1c6b63d6)), closes [univention/dev/internal/team-nubus#1131](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1131)

## [0.35.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.34.3...v0.35.0) (2025-04-29)


### Features

* Verify that the well known favicon URL works ([76a5dba](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/76a5dba793f9a246f9efef8a026eb8b510fbdb62)), closes [univention/dev/internal/team-nubus#889](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/889)


### Bug Fixes

* **testing-api:** Update base image version to 521:0.16.2-build-2025-04-17 ([e9a54a0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/e9a54a0dc39f47fb02577ad452529044617773a6))

## [0.34.3](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.34.2...v0.34.3) (2025-04-28)


### Bug Fixes

* **docker:** Raised UCS base image version to 0.16.2 ([7a63fe8](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/7a63fe8ceeae95851f9f18d9f779a3a53269d070)), closes [univention/dev/internal/team-nubus#996](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/996)
* **docs:** Added Playwright options. ([c1d3f38](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/c1d3f38e143243043886a9188453f6ae0b7a26ad)), closes [univention/dev/internal/team-nubus#996](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/996)
* **keycloak:** Fixing regex for portal domain. ([bc605cd](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/bc605cd30c93e6924fe0bc37cba1d03ecb3cefde)), closes [univention/dev/internal/team-nubus#996](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/996)
* **keycloak:** Refactoring unit tests. ([93a12f5](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/93a12f5be219e51e64133623c95d82f490c377de)), closes [univention/dev/internal/team-nubus#996](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/996)

## [0.34.2](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.34.1...v0.34.2) (2025-04-09)


### Bug Fixes

* **keycloak:** Added new Playwright class for Keycloak login page ([6507ca1](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/6507ca1fd3f0a990a060aa50735fd80135dbe0e2)), closes [univention/dev/internal/team-nubus#996](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/996)
* **keycloak:** Added Playwright page class for Keycloak login. ([fd0f8ed](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/fd0f8edd117ecab518e5ecaeba5f1be58780a693)), closes [univention/dev/internal/team-nubus#996](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/996)
* **keycloak:** Added tests for error message translations. ([840f35e](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/840f35e38c27045a2b2eac79814ee12f81ace5b6)), closes [univention/dev/internal/team-nubus#996](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/996)
* SPDX values and typos. ([c9921d9](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/c9921d97b4a4f2d751549c28ba6e22ed8b40336b)), closes [univention/dev/internal/team-nubus#996](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/996)

## [0.34.1](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.34.0...v0.34.1) (2025-04-07)


### Bug Fixes

* minimal python version ([092a693](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/092a69397e257d4517c704832d953c21e6f5d88f))

## [0.34.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.33.0...v0.34.0) (2025-04-07)


### Features

* **portal-server:** central navigation secret key is now password ([f9e0161](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/f9e0161d62879c7b9f244581a6adf940641f83bd)), closes [univention/dev/internal/team-nubus#1092](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1092)

## [0.33.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.32.0...v0.33.0) (2025-04-04)


### Features

* Omit default port in "base_url" ([f16a9e5](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/f16a9e54af6df36c1d7d1e2a0ed1a3f442329f37))
* Remove portal-base-url and keycloak-base-url from discovery script ([b13d7ab](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/b13d7ab750f844896d793e515edf3bd9eb1ea9df))

## [0.32.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.31.0...v0.32.0) (2025-03-24)


### Features

* Add new fixture KeycloakDeployment as "keycloak" ([15ec33a](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/15ec33a75cda06e11af5078d7d858bc3e4292b69))
* Add new utility "discover_url_parts_from_ingress" into KubernetesCluster ([4d9d312](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/4d9d3127fb362f66bbebe104694b2db71173ca6f))
* Discovered portal url and keycloak url are used for browser context ([7024807](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/7024807db97d39c0ac0aef2d278a9f7625f1e81a))
* PortalDeployment does discover base_url from Ingress ([e2a622e](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/e2a622ed54a8402dd3d1eed06666a33dab779b18))
* Remove fixtures "keycloak_base_url" and "portal_base_url" ([dba8fa3](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/dba8fa3f12aa7b39a13105aead8c10a0d54bfee7))


### Bug Fixes

* Remove wrong call to "wait_for_portal_sync" from layout test ([41d84de](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/41d84de7fc56458d6f0d5207f1aba7d18d287486))

## [0.31.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.30.0...v0.31.0) (2025-03-20)


### Features

* Verify that a deleted Portal Folder is removed from the link lists ([24c1ec9](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/24c1ec93f8f4b5ed420861709fd037c8d1778b9d))

## [0.30.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.29.1...v0.30.0) (2025-03-13)


### Features

* Add "retrying_fast" for things which can be polled frequently ([1ab412e](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/1ab412ee05a4d024bb5ff06a803394d2541e3795))
* Add coverage for Portal link lists of portal-extension ([89428cf](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/89428cfcf921fc5eb5bdc1b5b03b33d5a5311f27))
* Add fixture "portal_link_list", parametrized ([e8764fa](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/e8764fa7ccf502fdfad5bb68b3522513c023d727))
* Add utility method "PortalServerApi.get_portal" ([2470330](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/24703307ce2d6bb02b2a2347e3ce2b1c7cd367a2))
* Check link lists in the portal API ([8eddf2f](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/8eddf2ff362d988f6008bc707bb980f99c07a172))
* Discover UDM URL and credentials from deployment ([fedf9f3](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/fedf9f3f555834095105306030ab971171892d6b))
* Remove fixture "udm_rest_api_base_url" ([ea3a641](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/ea3a64154d3fff755ae2e68592dbfae0f61a1fec))
* Verify that deleted Portal Entries are removed from the Portal ([bfac49d](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/bfac49dbe81cd34af0a4f72b31e350cf61153a88))
* Verify that Portal Folders work in link lists ([5b66520](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/5b66520fb09aff30236756a5ca8c5343e2fdb9bf))
* Verify that quick links are part of the response from portal-server ([b39187a](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/b39187a99cba296856b392f534a5a4ae3b9b0b46))


### Bug Fixes

* Add configuration for mark "cookie_banner" ([df60432](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/df60432f9b5152855bd58fdce9eb00940dc50d71))
* Add pytest marks to ensure tests run when using the mark "acceptance_environment" ([157b174](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/157b1748f2206aeb41bcbd97b6c24fbb99c0daaf))
* Only create the async thread if needed ([93670cc](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/93670ccad2d729455b12c94741ca732cf3a09f3a))

## [0.29.1](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.29.0...v0.29.1) (2025-03-03)


### Bug Fixes

* Fix broken i18n tests to again use the correct fixture ([0a573e7](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/0a573e7bc7c1515075e15dcdea0294ae37ec063b))

## [0.29.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.28.0...v0.29.0) (2025-03-03)


### Features

* Add test of the portal server api endpoint "me" ([bb5660b](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/bb5660bc1e5b0d238cf0b790e9528677f6b7077b))


### Bug Fixes

* Use a regular user for "navigate_to_home_page_logged_in" ([8d5153e](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/8d5153e9b2040022d45aff6ecd193a35aedf4f72))

## [0.28.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.27.0...v0.28.0) (2025-02-28)


### Features

* Add base test to verify that the group "Domain Service Users" does exist ([3bfe27b](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/3bfe27bae96286828bd34c1cf3c2a0a12e43ca6c))
* Add fixture "portal" ([8747e00](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/8747e0068501e574248d1fe2983ea886feb7cbf3))
* Check the service account for the portal server ([ab7e6a8](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/ab7e6a83e3695e10f954c49c58f128a2fb0bb1b2))
* Verify that a member of "Domain Service Users" can read UDM Rest API objects ([f76e3f6](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/f76e3f68fdcef6d4cdf58fbd64ebd1b7bb82475b))
* Verify that domain service users can use the UDM Rest API ([36fa5ab](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/36fa5abf9b14da208ec971c6007672af7187f4fd))


### Bug Fixes

* Fallback to "default" when discovering the namespace in KubernetesCluster ([c53c76b](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/c53c76b5c2f1c1317a277ba6bff80509a63b705c))

## [0.27.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.26.0...v0.27.0) (2025-02-26)


### Features

* Remove xfail mark for Keycloak Ad Hoc Provisioning ([f46245c](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/f46245c1b5753b77e8dfb3c588dc44fe88590240))

## [0.26.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.25.1...v0.26.0) (2025-02-26)


### Features

* Bump ucs-base-image to use released apt sources ([d414db8](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/d414db81d600f3aa037b7466b5bae5fa4a450a67))

## [0.25.1](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.25.0...v0.25.1) (2025-02-25)


### Bug Fixes

* Add cleanup after Ad-Hoc Keycloak tests ([d36d44f](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/d36d44f4271379a6d1d59bef7adf19b11a9e27ec))

## [0.25.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.24.0...v0.25.0) (2025-02-25)


### Features

* Ad-Hoc Provisioning Keycloak tests setup and login ([15e09ad](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/15e09ad494ab9b2a165b2a35d72b8ac3cdcff227))

## [0.24.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.23.0...v0.24.0) (2025-01-09)


### Features

* Add "ChaosMeshFixture.pod_failure" ([5f8e350](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/5f8e3507fed1ef7572256b15cffb0e9e4feae231))
* Add "Experiment.wait_until_running" ([22e2511](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/22e25118b3b557c2d72952ea1be68753b57a7ce3))
* Add "k8s.scale_stateful_set" ([dba0087](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/dba00878fd6908ba7eda754ea528baa4d1da2eb0))
* Add "kubernetes" as a new dependency ([8b938db](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/8b938dbb94894b6b4d9d295c7768286d86705bfe))
* Add a support fixture for Chaos Mesh called "chaos" ([c53716d](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/c53716d06c5ff1c62acd96d33a5455e171fdfa63))
* Add fixtures to configure the Kubernetes client ([6822eb6](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/6822eb62046e42670629d8f2c023ee14ef23eff9))
* Add LDAPFixture to abstract the openldap deployment ([d30e461](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/d30e461f13781244feb175b4d4b62d4024ca2f25))
* Add provisioning_api fixture to provide details about the deployment ([9cd1bec](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/9cd1bece26d3bfc2c1e4e73d4c1e47ad509bf393))
* Add support to specify the release name via RELEASE_NAME env variable ([ac0b740](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/ac0b7406c53c71c8c0fec426bbf5e3f5c39a8243))
* Add utility function "add_release_prefix" ([0bb4238](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/0bb42382544278732af170ef0e081d065091a058))
* Check that nothing is lost during ldap leader switch ([26cc24d](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/26cc24dac2c32fbee09c29417d8aebf29eb78f6b))
* Check that the new ldap leader has the correct contextCSN ([b3f8e2f](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/b3f8e2ffafd6f125632845e349b0ff351547bbc3))
* Ensure that ldap test cases wait until all servers are ready ([7dad119](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/7dad119eda329766c9d146f9e71be6cf1dad1538))
* Handle namespace via kubernetes fixture ([1000741](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/1000741a144b30c8978ed14d828d08498c3640d8))
* Handle selection of the local port based on one starting number ([d8e98a8](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/d8e98a893e863b2fcf43b73610eecf5994f45217))
* Increase timeout for ldap to start up again ([c9e4565](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/c9e4565e8b56399ebc573ebfd796ea6f18d78f52))
* LDAPFixture.all_servers_reachable ([b86c852](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/b86c852ebbb6b521b66a1d16a913954b1aeb9f85))
* Prepare a consumer fixture running the eventloop in a thread ([134fe7d](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/134fe7de1de67fda0617af37661a366878abf02a))
* Stable subprocess handling with output forwarding ([6877c93](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/6877c932db09cd4efb3eb8dab617910efcf91305))
* Start test case simulating primary failure ([63d3c5a](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/63d3c5ab4610ce22c64cedddc715845fd747acc7))
* Test consumer receives message through provisioning ([2e512af](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/2e512af38e78e1f36727e192c001fc65eb724c9a))
* Update to playwright version v1.49.1-noble ([89e1b45](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/89e1b4584a8ea22c8552abdb9a46bc9c3b3d4a9e))
* Wait until the udm-listener did process the update ([9fc4cdf](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/9fc4cdf1bd67f05e8996c0806a3d48c0bd8e3b03))


### Bug Fixes

* Add credential discovery into provisioning api fixture ([2bb6265](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/2bb6265882b3c14bb6982cfed0186ed190cdb465))
* Add time to allow kubectl to establish the forwarding ([e1a4cdf](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/e1a4cdf64724ba5cd067e69ae4469b72fc344364))
* Also delete the ldap-notifier after deleting the server's pvcs ([8c0ae51](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/8c0ae51ec0541e476a4401b0f246d680a3cac620))
* Correctly support release name handling for the provisioning udm listener ([d86050b](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/d86050b8dfb168d627cbb93936863e69d497db36))
* Import ldap as pyldap to work around naming clash with the ldap fixture ([6c652ca](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/6c652ca823b89a9286a2d8aa4896409333ac9022))
* Increase timeout when waiting for listener logs ([f89b757](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/f89b757d3e599a4f8d05f73f4017063b989b70fc))
* Provide discovered target namespace via logging ([2dd4aa0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/2dd4aa0a4dae7ebd993f3a448c8683ce9b885837))
* Scale the notifier to zero in the ldap ha test ([366f712](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/366f71274f93c060281eb3604a9d35a5e70658ee))
* Use _create_server utility method in all cases ([9bcdf64](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/9bcdf64b29766bd592b2c8416e007e0350ff5352))
* Use restartable connection strategy for immediately bound ldap connection ([bcd335d](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/bcd335ddfaab5c63db584600fb53f4b1b8c9f500))

## [0.23.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.22.0...v0.23.0) (2025-01-08)


### Features

* guardian-ui test ([95f05e0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/95f05e085ae3b0d6635405ca7d1e7b94414d6f37))

## [0.22.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.21.0...v0.22.0) (2024-12-20)


### Features

* upgrade UCS base image to 2024-12-12 ([8b8c171](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/8b8c171ba12d3eec7a704ddabd30c80aff61f03c))

## [0.21.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.20.1...v0.21.0) (2024-12-16)


### Features

* test LDAP robustness with 2 primaries ([c162e0c](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/c162e0ce9eac3381fa4c6151d5066d325d09301a))

## [0.20.1](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.20.0...v0.20.1) (2024-12-13)


### Bug Fixes

* Add configuration for the marker "pytest.mark.groups" ([05d9ac3](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/05d9ac30fe6e49f6ece8aece7f9a47201df3f99a))

## [0.20.0](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/compare/v0.19.0...v0.20.0) (2024-12-09)


### Features

* Remove "column_header_type" from UCSGroupsPage ([696c985](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/696c9854ff4cf8c0f6f04c5f3b7d3373115ec20a))
* Remove "column_header_type" from UCSUsersPage ([bd0916a](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/bd0916a86646ec2273fba0d9f180eebbdecc8571))
* Remove unused class "UsersPage" ([a4e2bfb](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/commit/a4e2bfb415a56c737b1844a141fe608ac4708664))

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
