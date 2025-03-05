# Discovery from cluster

The test suite does need information about the deployment which we aim to
discover from the cluster through the Kubernetes API.

## Current status

The first step has been a proof of concept in a small shell script
`discover-env-from-cluster.sh`.

The next step will make direct use of the Kubernetes API from the [deployment
fixtures](./pod-deployment.md) so that the discovery will be more and more
automatic.

## Deployment fixtures

### Implementation suggestions

The deployment fixtures implement the discovery in a method
`_discover_from_cluster` which is described in the class `BaseDeployment`.

Discovered values should be exposed as attributes on the instance, so that test
cases which use the fixture have direct access.

### Examples

- `UdmRestApiDeployment` discovers the `base_url` from the `Ingress` object.
- `LdapDeployment` discovers usernames and passwords from various objects like
  `ConfigMap` and `Secret`.

## Customization via namespace annotations

Some details cannot be discovered with reasonable effort in the cluster. The
fixture `KubernetesCluster` does allow to override some "assumed" defaults with
annotations on the `Namespace` object.

All annotations use the prefix `nubus.univention.dev`.

### `nubus.univention.dev/ingress-http-port`

Allows to make the discovery mechanism aware of a custom ingress port for plain HTTP.

A typical use-case is a locally running cluster which has the ingress controller
exposed on port `8000`.

### `nubus.univention.dev/ingress-https-port`

The same as `nubus.univention.dev/ingress-http-port` for HTTPS.


