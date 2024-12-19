# LDAP High Availability Test Suite

## Overview

This test suite is designed to validate the high availability (HA) and data
replication capabilities of an LDAP server deployment, specifically focusing on
mirror mode robustness and data consistency during pod failures.

The tests are grouped into multiple files, so that every file does represent a
bigger scenario.

The tests in this folder cannot be executed as a whole suite and they do expect
that the deployment is prepared upfront. Every file has slightly different
requirements towards the deployment.

## Common

### Setup and Configuration

1. Set required environment variables:

   ```bash
   # Ensure that you have your kubernetes configuration selected.
   # Either by kubectx or via environment variables.
   export KUBECONFIG=/path/to/your/kubeconfig

   # Ensure that you have the target namespace selected
   # Either via kubens
   kubens your-namespace
   # Or via environment variables
   export DEPLOY_NAMESPACE=your-namespace
   ```

2. Enter the Python environment of the test suite, see `../README.md`:

   ```bash
   pipenv shell
   ```

## Test Scenario `test_ldap_ha.py`

The test performs the following key operations:
- Creates a predefined number of groups and users
- Randomly assigns users to multiple groups
- Moves users between groups
- Simulates a pod failure by deleting a primary LDAP server pod
- Verifies data consistency and replication across LDAP servers

### Deployment requirements

- Nubus deployment with at least the `ldap-server`, configured with 2 primaries.
- Alternative is a minimal deployment of the `ldap-server` chart together with
  the `ldap-notifier`.

### Running the Tests

Execute the test file using pytest:

```bash
pytest -lvs tests-ldap/test_ldap_ha.py
```

### Configuration Parameters

The test uses configuration from:
- `env_vars.py`: Loads Kubernetes configurations and LDAP credentials
- Environment variables for namespace and cluster access

Key configurable parameters are in the test file:
- `NUM_GROUPS`: Number of test groups to create (default: 10)
- `NUM_USERS`: Number of test users to create (default: 100)
- `NUM_USERS_TO_MOVE`: Number of users to move between groups (default: 50)

### Test Details

#### Workflow

1. Create initial test groups
2. Create test users
3. Randomly assign users to groups
4. Move users between groups
5. Delete primary LDAP server pod, by first removing its PVC
6. Continue group membership changes
7. Verify data consistency and replication

#### Verification Steps

- Compare LDAP server contents
- Verify group memberships
- Ensure all changes are preserved after pod recovery
- Validate data replication between LDAP servers


## Test scenario `test_first_primary_fails.py`

Various test cases check minimal scenarios around the switch of the primary ldap
server.

### Deployment Requirements

The following components are required:

- `ldap-server`

- The ldap server has to be scaled to two primaries. Proxies and secondaries can
  be scaled down to zero.
- Nubus deployment.
- Alternative: Deployment of `ldap-server`.


## Test scenario `test_provisioning.py`

This scenario does verify that the provisioning subsystem is receiving and
delivering messages when a change occurs.

### Deployment requirements

The following components are required:

- `ldap-server`
- `ldap-notifier`
- `provisioning`
- `provisioning-udm-listener`
- `udm-rest-api`

Either individually deployed or as a Nubus deployment.
