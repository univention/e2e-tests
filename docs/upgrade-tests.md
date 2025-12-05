# Upgrade Tests

Upgrade tests verify that Nubus functionality persists across version upgrades.

## How Upgrade Tests Work

Upgrade tests use pytest markers to separate pre and post-upgrade phases:

1. **Pre-upgrade (`@pytest.mark.pre_upgrade`)**: Tests that run on the old version
    - Set up test data/state that should persist through upgrade
    - Save any necessary information to `upgrade_artifacts_path` JSON file

2. **Upgrade**: System is upgraded to the new version

3. **Post-upgrade (`@pytest.mark.post_upgrade`)**: Tests that run on the new version
    - Verify the saved data/state still works correctly
    - Read information from `upgrade_artifacts_path` JSON file

## Example: 2FA Upgrade Test

See `tests/portal/upgrade/test_setup_2fa.py`:

- Pre-upgrade: Creates user, sets up 2FA, saves credentials to JSON
- Post-upgrade: Logs in with the saved 2FA credentials

## Running Locally

```bash
# Pre-upgrade phase
pytest -m pre_upgrade --upgrade-artifacts-path=/tmp/upgrade.json

# Post-upgrade phase
pytest -m post_upgrade --upgrade-artifacts-path=/tmp/upgrade.json
