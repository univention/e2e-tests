# LDAP High Availability Test Suite

## Overview

This test suite is designed to validate the high availability (HA) and data replication capabilities of an LDAP server deployment, specifically focusing on mirror mode robustness and data consistency during pod failures.

## Test Scenario

The test performs the following key operations:
- Creates a predefined number of groups and users
- Randomly assigns users to multiple groups
- Moves users between groups
- Simulates a pod failure by deleting a primary LDAP server pod
- Verifies data consistency and replication across LDAP servers

## Prerequisites

- Nubus deployment with at least the `ldap-server`, configured with 2 primaries.

## Setup and Configuration

1. Set required environment variables:
   ```bash
   export K8S_NAMESPACE=your-namespace
   export KUBECONFIG=/path/to/your/kubeconfig # only if you have more than one in your env
   ```

2. Install dependencies:
   ```bash
   pip install python-ldap kubernetes pytest
   ```

## Running the Tests

Execute the test suite using pytest:

```bash
pytest -lvs tests-ldap/test_ldap_ha.py
```

### Configuration Parameters

The test suite uses configuration from:
- `env_vars.py`: Loads Kubernetes configurations and LDAP credentials
- Environment variables for namespace and cluster access

Key configurable parameters (hardcoded in the file):
- `NUM_GROUPS`: Number of test groups to create (default: 10)
- `NUM_USERS`: Number of test users to create (default: 100)
- `NUM_USERS_TO_MOVE`: Number of users to move between groups (default: 50)

## Test Details

### Workflow

1. Create initial test groups
2. Create test users
3. Randomly assign users to groups
4. Move users between groups
5. Delete primary LDAP server pod, by first removing its PVC
6. Continue group membership changes
7. Verify data consistency and replication

### Verification Steps

- Compare LDAP server contents
- Verify group memberships
- Ensure all changes are preserved after pod recovery
- Validate data replication between LDAP servers
