# testing-api

Testing api for nubus e2e tests

- **Version**: 0.1.0
- **Type**: application
- **AppVersion**: 0.0.1
-

## Introduction

This chart installs the testing-api container.
It supports the nubus e2e tests by exposing functionality otherwise not reachable from outside the cluster.

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| oci://artifacts.software-univention.de/nubus/charts | nubus-common | ^0.12.x |

## Values

<table>
	<thead>
		<th>Key</th>
		<th>Type</th>
		<th>Default</th>
		<th>Description</th>
	</thead>
	<tbody>
		<tr>
			<td>extraSecrets</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td>Optionally specify a secret to create (primarily intended to be used in development environments to provide custom certificates)</td>
		</tr>
		<tr>
			<td>global.imagePullPolicy</td>
			<td>string</td>
			<td><pre lang="json">
"IfNotPresent"
</pre>
</td>
			<td>Define an ImagePullPolicy.  Ref.: https://kubernetes.io/docs/concepts/containers/images/#image-pull-policy  "IfNotPresent" => The image is pulled only if it is not already present locally. "Always" => Every time the kubelet launches a container, the kubelet queries the container image registry to             resolve the name to an image digest. If the kubelet has a container image with that exact digest cached             locally, the kubelet uses its cached image; otherwise, the kubelet pulls the image with the resolved             digest, and uses that image to launch the container. "Never" => The kubelet does not try fetching the image. If the image is somehow already present locally, the            kubelet attempts to start the container; otherwise, startup fails.</td>
		</tr>
		<tr>
			<td>global.imagePullSecrets</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td>Credentials to fetch images from private registry Ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/  imagePullSecrets:   - "docker-registry" </td>
		</tr>
		<tr>
			<td>global.imageRegistry</td>
			<td>string</td>
			<td><pre lang="json">
"artifacts.software-univention.de"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>image.imagePullPolicy</td>
			<td>string</td>
			<td><pre lang="json">
"IfNotPresent"
</pre>
</td>
			<td>The pull policy of the container image.  This setting has higher precedence than global.imagePullPolicy.</td>
		</tr>
		<tr>
			<td>image.registry</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Container registry address. This setting has higher precedence than global.registry.</td>
		</tr>
		<tr>
			<td>image.repository</td>
			<td>string</td>
			<td><pre lang="json">
"nubus-dev/images/testing-api"
</pre>
</td>
			<td>The path to the container image.</td>
		</tr>
		<tr>
			<td>image.tag</td>
			<td>string</td>
			<td><pre lang="json">
"0.18.0"
</pre>
</td>
			<td>The tag of the container image. (This is replaced with an appropriate value during the build process of the Helm chart.)</td>
		</tr>
		<tr>
			<td>testingApi.config.logLevel</td>
			<td>string</td>
			<td><pre lang="json">
"INFO"
</pre>
</td>
			<td>Log level for the selfservice listener. valid values are: ERROR WARNING, INFO, DEBUG</td>
		</tr>
		<tr>
			<td>testingApi.ingress.host</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>testingApi.ingress.ingressClassName</td>
			<td>string</td>
			<td><pre lang="json">
"nginx"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>testingApi.ingress.tls.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>testingApi.ingress.tls.secretName</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>testingApi.ldap</td>
			<td>object</td>
			<td><pre lang="json">
{
  "auth": {
    "bindDn": "",
    "credentialSecret": {
      "key": "password",
      "name": ""
    }
  },
  "baseDn": "",
  "primaryConnection": {
    "host": "",
    "port": "389"
  },
  "secondaryConnection": {
    "host": "",
    "port": "389"
  }
}
</pre>
</td>
			<td>LDAP settings.</td>
		</tr>
		<tr>
			<td>testingApi.ldap.auth</td>
			<td>object</td>
			<td><pre lang="json">
{
  "bindDn": "",
  "credentialSecret": {
    "key": "password",
    "name": ""
  }
}
</pre>
</td>
			<td>LDAP authentication parameters.</td>
		</tr>
		<tr>
			<td>testingApi.ldap.auth.bindDn</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>LDAP bind DN. (user to authenticate with LDAP server)</td>
		</tr>
		<tr>
			<td>testingApi.ldap.auth.credentialSecret</td>
			<td>object</td>
			<td><pre lang="json">
{
  "key": "password",
  "name": ""
}
</pre>
</td>
			<td>LDAP bind password secret reference.</td>
		</tr>
		<tr>
			<td>testingApi.ldap.baseDn</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>The LDAP base DN to use when connecting.</td>
		</tr>
		<tr>
			<td>testingApi.ldap.primaryConnection</td>
			<td>object</td>
			<td><pre lang="json">
{
  "host": "",
  "port": "389"
}
</pre>
</td>
			<td>LDAP server primary headless service connection parameters.</td>
		</tr>
		<tr>
			<td>testingApi.ldap.primaryConnection.host</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>LDAP host.</td>
		</tr>
		<tr>
			<td>testingApi.ldap.primaryConnection.port</td>
			<td>string</td>
			<td><pre lang="json">
"389"
</pre>
</td>
			<td>LDAP port.</td>
		</tr>
		<tr>
			<td>testingApi.ldap.secondaryConnection</td>
			<td>object</td>
			<td><pre lang="json">
{
  "host": "",
  "port": "389"
}
</pre>
</td>
			<td>LDAP server secondary headless service connection parameters.</td>
		</tr>
		<tr>
			<td>testingApi.ldap.secondaryConnection.host</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>LDAP host.</td>
		</tr>
		<tr>
			<td>testingApi.ldap.secondaryConnection.port</td>
			<td>string</td>
			<td><pre lang="json">
"389"
</pre>
</td>
			<td>LDAP port.</td>
		</tr>
	</tbody>
</table>

