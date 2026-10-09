# Container settings schema and field guide

This document describes the JSON object in `container_settings.json`. The file is the contents of a Dataiku DSS `containerSettings` object (rather than the whole `general-settings.json` document). It contains instance-level options, image build configurations, execution configurations, and generic Kubernetes overrides.

## Scope and interpretation

The schema below is inferred from the supplied instance JSON. It documents fields that are present in the sample and keeps objects extensible because DSS may add version-specific fields. It is not a vendor-published or version-independent contract. The sample has only `DOCKER` and `DKU_IN_CLUSTER` image builder types and `KUBERNETES` execution types; it does not establish schemas for other possible engines.

Several fields have empty arrays, so their item structure cannot be determined from this file alone (`additionalLabels`, `namespaceLabels`, `hostPathVolumes`, `dockerResources`, `customRequests`, `serviceAnnotations` are not present here; arrays in this document are scoped only to fields actually found). Descriptions marked **inferred** are based on the key name and example values, and should be confirmed in the matching DSS release.

Sentinel-like values of `-1` appear for resource quantities and shared-memory size. The file does not explicitly define their semantics; this guide describes them as likely “unset/default” values rather than asserting that as a guaranteed rule.

## Structure at a glance

```text
containerSettings
├── instance switches and defaults
├── buildConfigs[]
│   ├── dockerBuilderConfig
│   └── dkuInClusterBuilderConfig
├── executionConfigs[]
│   ├── dockerRuntimeConfig
│   └── kubernetesRuntimeConfig
│       └── kubernetesResources
└── executionConfigsGenericOverrides
    └── kubernetesResources
```

## JSON Schema (Draft 2020-12)

This schema models the observed fields and value types. `additionalProperties: true` is used deliberately to tolerate fields from other DSS versions. Fields are not marked required, since this one exported object cannot show which fields are optional in all supported configurations.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.invalid/dataiku/container-settings.schema.json",
  "title": "Observed Dataiku DSS containerSettings",
  "type": "object",
  "properties": {
    "autoRebuildCDEImageOnPluginChange": { "type": "boolean" },
    "buildConfigs": {
      "type": "array",
      "items": { "$ref": "#/$defs/buildConfig" }
    },
    "cdeEnabled": { "type": "boolean" },
    "cdePluginSupport": { "type": "boolean" },
    "defaultExecutionConfig": { "type": "string" },
    "defaultExecutionConfigForVisualRecipesWorkloads": { "type": "string" },
    "defaultWebappsDockerExposition": { "$ref": "#/$defs/dockerWebAppExposition" },
    "defaultWebappsK8SExposition": { "$ref": "#/$defs/kubernetesWebAppExposition" },
    "executionConfigs": {
      "type": "array",
      "items": { "$ref": "#/$defs/executionConfig" }
    },
    "executionConfigsGenericOverrides": { "$ref": "#/$defs/genericOverrides" }
  },
  "$defs": {
    "buildConfig": {
      "type": "object",
      "properties": {
        "baseImageType": { "type": "string", "examples": ["EXEC"] },
        "dkuInClusterBuilderConfig": { "$ref": "#/$defs/inClusterBuilder" },
        "dockerBuilderConfig": { "$ref": "#/$defs/dockerBuilder" },
        "imageBuilderType": {
          "type": "string",
          "enum": ["DOCKER", "DKU_IN_CLUSTER"]
        },
        "isFinal": { "type": "boolean" },
        "name": { "type": "string" },
        "properties": { "$ref": "#/$defs/propertyList" }
      },
      "additionalProperties": true
    },
    "inClusterBuilder": {
      "type": "object",
      "properties": {
        "additionalLabels": { "$ref": "#/$defs/openArray" },
        "baseImageRegistryConfig": { "$ref": "#/$defs/registryConfig" },
        "createNamespace": { "type": "boolean" },
        "kubeConfigPath": { "type": "string" },
        "kubernetesNamespace": { "type": "string" },
        "kubernetesResources": { "$ref": "#/$defs/kubernetesResources" },
        "namespaceLabels": { "$ref": "#/$defs/openArray" },
        "nodeSelector": { "type": "string" },
        "pushConfigs": {
          "type": "array",
          "items": { "$ref": "#/$defs/pushConfig" }
        },
        "stagingRegistryConfig": { "$ref": "#/$defs/registryConfig" }
      },
      "additionalProperties": true
    },
    "dockerBuilder": {
      "type": "object",
      "properties": {
        "dockerHost": { "type": "string" },
        "dockerTLSVerify": { "type": "boolean" },
        "pushConfigs": {
          "type": "array",
          "items": { "$ref": "#/$defs/pushConfig" }
        }
      },
      "additionalProperties": true
    },
    "registryConfig": {
      "type": "object",
      "properties": {
        "prePushMode": { "type": "string", "examples": ["NONE"] }
      },
      "additionalProperties": true
    },
    "pushConfig": {
      "type": "object",
      "properties": {
        "prePushMode": { "type": "string", "examples": ["ECR", "NONE"] },
        "repositoryURL": { "type": "string" }
      },
      "additionalProperties": true
    },
    "executionConfig": {
      "type": "object",
      "properties": {
        "DKU_TMPDIR": { "type": "string" },
        "allowedGroups": { "type": "array", "items": { "type": "string" } },
        "dockerRuntimeConfig": { "$ref": "#/$defs/dockerRuntime" },
        "imageBuildConfig": { "type": "string" },
        "isFinal": { "type": "boolean" },
        "kubernetesRuntimeConfig": { "$ref": "#/$defs/kubernetesRuntime" },
        "name": { "type": "string" },
        "properties": { "$ref": "#/$defs/propertyList" },
        "type": { "type": "string", "enum": ["KUBERNETES"] },
        "usableBy": { "type": "string", "examples": ["ALL"] },
        "workloadType": {
          "type": "string",
          "examples": ["USER_CODE", "VISUAL_RECIPES"]
        }
      },
      "additionalProperties": true
    },
    "dockerRuntime": {
      "type": "object",
      "properties": {
        "dockerNetwork": { "type": "string" },
        "dockerResources": { "$ref": "#/$defs/openArray" },
        "dockerTLSVerify": { "type": "boolean" }
      },
      "additionalProperties": true
    },
    "kubernetesRuntime": {
      "type": "object",
      "properties": {
        "createNamespace": { "type": "boolean" },
        "customSHMValueMB": { "type": "integer" },
        "enableCustomSHM": { "type": "boolean" },
        "ensureNamespaceCompliance": { "type": "boolean" },
        "hostPathVolumes": { "$ref": "#/$defs/openArray" },
        "kubeConfigPath": { "type": "string" },
        "kubernetesNamespace": { "type": "string" },
        "kubernetesResources": { "$ref": "#/$defs/kubernetesResources" },
        "namespaceLabels": { "$ref": "#/$defs/openArray" },
        "noImplicitK8sClusterAndNoDefaultClusterId": { "type": "boolean" },
        "nodeSelector": { "type": "string" },
        "properties": { "$ref": "#/$defs/propertyList" },
        "tolerations": { "type": "string" }
      },
      "additionalProperties": true
    },
    "kubernetesResources": {
      "type": "object",
      "properties": {
        "cpuLimit": { "type": "number" },
        "cpuRequest": { "type": "number" },
        "customLimits": {
          "type": "array",
          "items": { "$ref": "#/$defs/customResource" }
        },
        "customRequests": {
          "type": "array",
          "items": { "$ref": "#/$defs/customResource" }
        },
        "memLimitMB": { "type": "integer" },
        "memRequestMB": { "type": "integer" }
      },
      "additionalProperties": true
    },
    "customResource": {
      "type": "object",
      "properties": {
        "isFinal": { "type": "boolean" },
        "key": { "type": "string" },
        "secret": { "type": "boolean" },
        "value": { "type": "string" }
      },
      "additionalProperties": true
    },
    "propertyList": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "key": { "type": "string" },
          "secret": { "type": "boolean" },
          "value": { "type": "string" }
        },
        "additionalProperties": true
      }
    },
    "genericOverrides": {
      "type": "object",
      "properties": {
        "createNamespace": { "type": "boolean" },
        "customSHMValueMB": { "type": "integer" },
        "enableCustomSHM": { "type": "boolean" },
        "ensureNamespaceCompliance": { "type": "boolean" },
        "hostPathVolumes": { "$ref": "#/$defs/openArray" },
        "kubernetesResources": { "$ref": "#/$defs/kubernetesResources" },
        "namespaceLabels": { "$ref": "#/$defs/openArray" },
        "noImplicitK8sClusterAndNoDefaultClusterId": { "type": "boolean" },
        "properties": { "$ref": "#/$defs/propertyList" }
      },
      "additionalProperties": true
    },
    "dockerWebAppExposition": {
      "type": "object",
      "properties": {
        "params": {
          "type": "object",
          "properties": { "allInterfaces": { "type": "boolean" } },
          "additionalProperties": true
        },
        "type": { "type": "string", "examples": ["docker_direct"] }
      },
      "additionalProperties": true
    },
    "kubernetesWebAppExposition": {
      "type": "object",
      "properties": {
        "params": {
          "type": "object",
          "properties": {
            "serviceAnnotations": { "$ref": "#/$defs/openArray" },
            "useService": { "type": "boolean" }
          },
          "additionalProperties": true
        },
        "type": { "type": "string", "examples": ["port_forward"] }
      },
      "additionalProperties": true
    },
    "openArray": { "type": "array", "items": {} }
  },
  "additionalProperties": true
}
```

## Field-by-field documentation

### Top-level settings

| Field | JSON type | Example from file | Description |
|---|---|---|---|
| `autoRebuildCDEImageOnPluginChange` | Boolean | `false` | Controls automatic rebuilding of the containerized DSS engine image when a plugin changes. The key name indicates the trigger and target. |
| `buildConfigs` | Array of objects | 2 entries | Image build configurations. Each names a builder implementation and contains builder-specific settings and image push destinations. |
| `cdeEnabled` | Boolean | `true` | Enables the containerized DSS engine feature. |
| `cdePluginSupport` | Boolean | `true` | **Inferred:** controls plugin support in the containerized DSS engine. |
| `defaultExecutionConfig` | String | `eks-default` | Name of the instance-wide default container execution configuration. References an entry in `executionConfigs[].name`. |
| `defaultExecutionConfigForVisualRecipesWorkloads` | String | `CDE-1CPU-8GB` | Default execution config for visual recipe workloads. This is also a name in `executionConfigs`. |
| `defaultWebappsDockerExposition` | Object | `docker_direct` | Default method and parameters for exposing web app backends running with Docker. |
| `defaultWebappsK8SExposition` | Object | `port_forward` | Default method and parameters for exposing web app backends running on Kubernetes. |
| `executionConfigs` | Array of objects | 10 entries | Runtime configurations that specify engine, image builder, workload type, access, resources, and Kubernetes behavior. |
| `executionConfigsGenericOverrides` | Object | See JSON | Generic Kubernetes settings used as overrides/defaults. Its fields overlap with `kubernetesRuntimeConfig`; it also includes `properties`. |

### Build configuration: common fields (`buildConfigs[]`)

| Field | JSON type | Example | Description |
|---|---|---|---|
| `name` | String | `Build with Docker (locally)` | Human-readable config name. Other settings reference it by name, notably `executionConfigs[].imageBuildConfig`. |
| `imageBuilderType` | String | `DOCKER`, `DKU_IN_CLUSTER` | Builder implementation. These are the two values seen in this file; they should not be treated as the complete DSS enum. |
| `baseImageType` | String | `EXEC` | Base image family/type. Only `EXEC` appears in the supplied file. |
| `isFinal` | Boolean | `false` | **Inferred:** likely marks the setting as final or protected from overrides. Confirm its semantics in the relevant release. |
| `properties` | Array of property objects | `[]` | Additional key/value properties. Each non-empty property follows the shape described under Property entries below. |
| `dockerBuilderConfig` | Object | Present on both entries | Docker builder settings. Its `dockerHost` field is omitted in one entry, showing that the field is not always serialized. |
| `dkuInClusterBuilderConfig` | Object | Present on both entries | Settings for a builder running in Kubernetes. |

The sample contains both builder-specific subobjects for each build config, even though `imageBuilderType` selects the active builder. The dump alone does not show whether the inactive subobject is ignored, retained as a default, or used for another purpose. Preserve it when editing an existing object unless the DSS UI for that version demonstrates otherwise.

#### Docker builder: `dockerBuilderConfig`

| Field | JSON type | Example | Description |
|---|---|---|---|
| `dockerHost` | String | `""` | Docker daemon endpoint. Empty string appears to select the default/local Docker daemon; this is an inference. |
| `dockerTLSVerify` | Boolean | `false` | Whether TLS peer verification is enabled for Docker daemon access. |
| `pushConfigs` | Array of objects | One entry | Image publishing destinations and any pre-push hook/auth mode. |

#### In-cluster builder: `dkuInClusterBuilderConfig`

| Field | JSON type | Example | Description |
|---|---|---|---|
| `additionalLabels` | Array | `[]` | **Inferred:** additional Kubernetes labels for builder resources. Item structure is not visible because the array is empty. |
| `baseImageRegistryConfig` | Object | `{"prePushMode":"NONE"}` | Registry-related configuration for base images. |
| `createNamespace` | Boolean | `true` | Whether the namespace should be created if it does not already exist. |
| `kubeConfigPath` | String | filesystem path | Kubeconfig path used by the in-cluster builder setup. |
| `kubernetesNamespace` | String | `tam-global-container-builder` | Namespace where builder resources run. |
| `kubernetesResources` | Object | CPU/memory fields | Resource requests/limits for the builder workload. See Kubernetes resources below. |
| `namespaceLabels` | Array | `[]` | **Inferred:** labels assigned to the namespace. Item structure cannot be recovered from an empty array. |
| `nodeSelector` | String, optional | YAML text | Kubernetes scheduling selector in text form. One build config includes a YAML `nodeSelector` block; the other omits this key. |
| `pushConfigs` | Array of objects | ECR destination | Publishing target(s) for images. |
| `stagingRegistryConfig` | Object | `{"prePushMode":"NONE"}` | Registry configuration used for staging images. Exact behavior is inferred from the name. |

#### Registry settings: `baseImageRegistryConfig`, `stagingRegistryConfig`

| Field | JSON type | Example | Description |
|---|---|---|---|
| `prePushMode` | String | `NONE` | Selects a pre-push mode/hook. The sample also uses `ECR` in push targets. The full enum depends on the installation and version. |

#### Push target: `pushConfigs[]`

| Field | JSON type | Example | Description |
|---|---|---|---|
| `prePushMode` | String | `ECR`, `NONE` | Pre-push authentication/integration mode selected for the destination. |
| `repositoryURL` | String | Registry hostname | Image registry/repository endpoint. The sample contains an AWS ECR hostname; redact account and registry details before sharing externally. |

### Execution configurations: `executionConfigs[]`

| Field | JSON type | Example | Description |
|---|---|---|---|
| `name` | String | `eks-default` | Name of this runtime config. Used by top-level defaults and other settings. |
| `type` | String | `KUBERNETES` | Runtime engine. Only Kubernetes configs occur in this file. |
| `imageBuildConfig` | String | `Build on K8s` | Name of the image build config used to build/publish images for this runtime. Must match a `buildConfigs[].name` entry to be a valid reference. |
| `workloadType` | String | `USER_CODE`, `VISUAL_RECIPES` | Workload category accepted by this config. Those values are observed examples, not a guaranteed complete enumeration. |
| `usableBy` | String | `ALL` | Access mode for users/groups. Only `ALL` is shown. |
| `allowedGroups` | Array of strings | `[]` | Group names allowed to use the config when access is restricted. Empty in all provided entries. |
| `DKU_TMPDIR` | String | `/tmp` | Temporary directory path provided to workload execution. |
| `isFinal` | Boolean | `false` | **Inferred:** likely a final/locked marker. Validate the semantics before setting it. |
| `properties` | Array of property objects | `readOnlyRootFilesystem=true` | Extra runtime properties. Used in this file for a root filesystem setting and CDE memory-overhead tuning. |
| `dockerRuntimeConfig` | Object | `dockerNetwork=host` | Docker runtime settings. It is present on entries whose `type` is Kubernetes; therefore, presence alone does not determine the selected runtime engine. |
| `kubernetesRuntimeConfig` | Object | namespace/resources/scheduling | Kubernetes runtime behavior for namespace, placement, volumes, shared memory, and resources. |

#### Docker runtime: `dockerRuntimeConfig`

| Field | JSON type | Example | Description |
|---|---|---|---|
| `dockerNetwork` | String | `host` | Docker network mode. |
| `dockerResources` | Array | `[]` | **Inferred:** Docker resource restrictions. Item shape is not present in this sample. |
| `dockerTLSVerify` | Boolean | `false` | Docker TLS verification option. |

#### Kubernetes runtime: `kubernetesRuntimeConfig`

| Field | JSON type | Example | Description |
|---|---|---|---|
| `createNamespace` | Boolean | `true` | Whether DSS creates the target namespace when required. |
| `customSHMValueMB` | Integer | `-1` | Custom shared memory size in MB. `-1` appears to represent an unset/default size, inferred from the value. |
| `enableCustomSHM` | Boolean | `true` or `false` | Whether custom shared memory is enabled. |
| `ensureNamespaceCompliance` | Boolean | `true` or `false` | **Inferred:** whether DSS applies or checks namespace policy/compliance requirements. |
| `hostPathVolumes` | Array | `[]` | Host path volumes mounted into workload pods. No item examples are present. |
| `kubeConfigPath` | String, sometimes omitted | `""` | Explicit kubeconfig path. An empty or absent value may mean DSS selects credentials/cluster elsewhere; that interpretation is inferred. |
| `kubernetesNamespace` | String/template | `tam-global-${dssUserLogin}` | Target namespace. `${dssUserLogin}` is a literal template placeholder in the sample, apparently resolved per user. |
| `kubernetesResources` | Object | Resource settings | CPU, memory, and additional Kubernetes resource requests/limits. |
| `namespaceLabels` | Array | `[]` | **Inferred:** labels to apply to the namespace. No member examples are present. |
| `noImplicitK8sClusterAndNoDefaultClusterId` | Boolean | `false` | **Inferred:** controls behavior when no explicit/default Kubernetes cluster ID is set. Confirm the meaning in the matching DSS version. |
| `nodeSelector` | String | YAML text | Kubernetes node selector, serialized as a string rather than a JSON object. Examples select `workerType: nongpu`, `workerType: gpu`, `role: gpuxsmall`, or `ec2-type: t3large`. |
| `tolerations` | String, optional | `""` or YAML text | Kubernetes pod tolerations, serialized as a string. The GPU test config contains a `NoSchedule` toleration; other entries omit the field. |

#### Kubernetes resources: `kubernetesResources`

This object occurs under both the in-cluster builder and Kubernetes runtime settings, and also inside `executionConfigsGenericOverrides`.

| Field | JSON type | Examples | Description |
|---|---|---|---|
| `cpuRequest` | Number | `-1.0`, `0.5`, `1.0`, `1.5`, `2.0` | CPU request. Kubernetes quantities are conventionally measured in cores here. `-1` appears to be a sentinel for default/unset. |
| `cpuLimit` | Number | `-1.0`, `0.5`, `1.0`, `2.0` | CPU limit, likely in cores. `-1` appears to be default/unset. |
| `memRequestMB` | Integer | `-1`, `500`, `2000`, `4000`, `8000`, `12000` | Memory request in MB. |
| `memLimitMB` | Integer | `-1`, `3000`, `4000`, `6000`, `12000`, `16000` | Memory limit in MB. |
| `customRequests` | Array of custom resource objects | `[]` throughout | Additional Kubernetes resource requests. Empty in this file, so there is no sample item. |
| `customLimits` | Array of custom resource objects | `nvidia.com/gpu: 1` or `[]` | Additional Kubernetes resource limits. GPU configs show one custom limit object. |

Observed custom resource object fields:

| Field | JSON type | Example | Description |
|---|---|---|---|
| `key` | String | `nvidia.com/gpu` | Kubernetes resource name. |
| `value` | String | `1` | Resource quantity encoded as a string. |
| `secret` | Boolean | `false` | Flag whose exact interpretation is not specified by the sample; likely secret/protected-value handling. |
| `isFinal` | Boolean | `false` | **Inferred:** likely marks this entry as final or non-overridable. |

### Property entries

`properties` is an array of objects used in build config or execution config. The supplied non-empty entries have the following shape:

| Field | JSON type | Examples | Description |
|---|---|---|---|
| `key` | String | `readOnlyRootFilesystem`, `dku.cde.memoryOverheadFactor` | Property identifier. The property namespace/name determines its meaning. |
| `value` | String | `true`, `0.2` | Property value stored as text, including values that look boolean or numeric. |
| `secret` | Boolean | `false` | Marks whether the property value is secret. |

The observed settings suggest `readOnlyRootFilesystem=true` controls the container root filesystem and `dku.cde.memoryOverheadFactor=0.2` configures CDE memory overhead. These specific effects are inferred from the keys; the JSON itself does not provide descriptions.

### Default web app exposure objects

#### `defaultWebappsDockerExposition`

| Field | JSON type | Example | Description |
|---|---|---|---|
| `type` | String | `docker_direct` | Exposure strategy identifier. Only this mode occurs in the file. |
| `params` | Object | — | Parameters for the selected strategy. |
| `params.allInterfaces` | Boolean | `false` | **Inferred:** whether the Docker-backed endpoint listens on all network interfaces. |

#### `defaultWebappsK8SExposition`

| Field | JSON type | Example | Description |
|---|---|---|---|
| `type` | String | `port_forward` | Exposure strategy identifier. Only this mode occurs in the file. |
| `params` | Object | — | Parameters for the selected strategy. |
| `params.serviceAnnotations` | Array | `[]` | Kubernetes service annotations. Empty in the sample, so item shape is unknown. |
| `params.useService` | Boolean | `false` | **Inferred:** whether a Kubernetes Service resource is used for exposure. |

### Generic overrides: `executionConfigsGenericOverrides`

The object contains:

| Field | JSON type | Description |
|---|---|---|
| `createNamespace` | Boolean | Namespace creation behavior used by generic overrides. |
| `customSHMValueMB` | Integer | Custom shared-memory value in MB; sample value is `-1`. |
| `enableCustomSHM` | Boolean | Whether to use the custom shared-memory setting. |
| `ensureNamespaceCompliance` | Boolean | Namespace compliance setting; exact semantics are inferred. |
| `hostPathVolumes` | Array | Host path volumes; empty in sample, member shape unknown. |
| `kubernetesResources` | Object | Generic resource defaults, with the same fields as above. All quantities in the sample are `-1`. |
| `namespaceLabels` | Array | Namespace labels; empty in sample, member shape unknown. |
| `noImplicitK8sClusterAndNoDefaultClusterId` | Boolean | Cluster-selection behavior; exact semantics inferred from the name. |
| `properties` | Array of property objects | Generic properties; empty in sample. |

## Values and references observed in this file

### Builder and execution names

The `defaultExecutionConfig` and `defaultExecutionConfigForVisualRecipesWorkloads` values refer to runtime entries by `executionConfigs[].name`. Every `executionConfigs[].imageBuildConfig` value should refer to a `buildConfigs[].name` entry. In this file, the build config names are `Build with Docker (locally)` and `Build on K8s`.

The runtime names in the sample are `eks-default`, `eks-gpu`, `testconfig`, `ekscpu`, `CDE-1CPU-8GB`, `CDE-TESTING-BROKEN`, `general_2GB_0.5CPU`, `general_4GB_1CPU`, `general_8GB_2CPU`, and `CDE-2CPU-16GB`.

### Workload categories

Observed `workloadType` values:

- `USER_CODE` — used on the user-code runtime entries.
- `VISUAL_RECIPES` — used on the CDE visual recipe entries.

These labels describe observed values only. This document does not guarantee they are the only valid options.

## Shape limitations in the source file

The following arrays are empty in the provided JSON, so their item definitions cannot be specified reliably from this example:

- `buildConfigs[].dkuInClusterBuilderConfig.additionalLabels`
- `buildConfigs[].dkuInClusterBuilderConfig.namespaceLabels`
- `executionConfigs[].dockerRuntimeConfig.dockerResources`
- `executionConfigs[].kubernetesRuntimeConfig.hostPathVolumes`
- `executionConfigs[].kubernetesRuntimeConfig.namespaceLabels`
- `executionConfigs[].kubernetesRuntimeConfig.kubernetesResources.customRequests`
- `executionConfigs[].kubernetesRuntimeConfig.kubernetesResources.customLimits` is non-empty only in GPU entries, so its observed object shape is documented above.
- `executionConfigsGenericOverrides.hostPathVolumes`
- `executionConfigsGenericOverrides.namespaceLabels`
- `executionConfigsGenericOverrides.kubernetesResources.customRequests`
- `executionConfigsGenericOverrides.kubernetesResources.customLimits`
- `defaultWebappsK8SExposition.params.serviceAnnotations`

To complete those item schemas, obtain a non-empty instance of each setting from the same DSS release or inspect the corresponding UI-generated configuration.
