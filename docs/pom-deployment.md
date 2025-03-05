# Object Model for Deployments

Some of the tests depend on information about the deployment into a Kubernetes
cluster. There is a fixture to provide information about the cluster itself and
a collection of fixtures to provide information about the deployed components.

The fixtures are intentionally per component, so that they can also be used with
partial deployments during development when one wants to run a subset of the
tests suite.


## Advanced functionality

Some fixtures offer advanced functionality like automatic port forwarding in the
`LdapDeployment` case.

These features should be designed in a way so that they are not causing
unnecessary overhead during the regular usage of the fixture.
