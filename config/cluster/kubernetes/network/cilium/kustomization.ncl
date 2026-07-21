let { contracts, .. } = import "../../../../libs/contracts.ncl" in
{
  cluster.kubernetes.network.cilium.kustomization = {
    apiVersion = "kustomize.config.k8s.io/v1beta1",
    kind = "Kustomization",
    helmCharts = [
      {
        name = "cilium",
        releaseName = "cilium",
        namespace = cluster.kubernetes.network.cilium.namespace.name,
        repo = "oci://quay.io/cilium/charts/cilium",
        version = cluster.kubernetes.network.cilium.version,
        valuesInline = {
          bpf = { hostLegacyRouting = false, masquerade = true },
          cgroup = {
            autoMount = { enabled = false },
            hostRoot = "/sys/fs/cgroup"
          },
          egressGateway = {
            enabled = true,
          },
          envoyConfig = {
            secretsNamespace = {
              create = false,
              name = namespace,
            },
          },
          gatewayAPI = {
            enabled = true,
            enableAlpn = true,
            enableAppProtocol = true,
            secretsNamespace = {
              create = false,
              name = namespace,
            },
          },
          hostFirewall = {
            enabled = true,
          },
          hubble = {
            enabled = true,
            relay = { enabled = true },
            ui = { enabled = true },
          },
          ipam = { mode = "kubernetes" },
          ipv6 = { enabled = true },
          kubeProxyReplacement = true,
          k8sServiceHost = "localhost",
          k8sServicePort = 7445,
          nodeIPAM = {
            enabled = true,
          },
          operator = { replicas = 1 },
          securityContext = {
            capabilities = {
              ciliumAgent = [
                "CHOWN",
                "KILL",
                "NET_ADMIN",
                "NET_RAW",
                "IPC_LOCK",
                "SYS_ADMIN",
                "SYS_RESOURCE",
                "DAC_OVERRIDE",
                "FOWNER",
                "SETGID",
                "SETUID"
              ],
              cleanCiliumState = ["NET_ADMIN", "SYS_ADMIN", "SYS_RESOURCE"]
            }
          },
          tls = {
            secretsNamespace = {
              create = false,
              name = namespace,
            },
          },
        },
      }
    ],
    replacements = [
      {
        sourceValue =
          contracts.Reference
          & {
            kind = "pulumi/secret",
            type = "str",
            path = "cluster.kubernetes.network.cilium.cilium-ca.ca.crt",
          },
        targets = [
          {
            select = { name = "cilium-ca", kind = "Secret" },
            fieldPaths = ["data.[ca.crt]"]
          }
        ]
      },
      {
        sourceValue =
          contracts.Reference
          & {
            kind = "pulumi/secret",
            type = "str",
            path = "cluster.kubernetes.network.cilium.cilium-ca.ca.key",
          },
        targets = [
          {
            select = { name = "cilium-ca", kind = "Secret" },
            fieldPaths = ["data.[ca.key]"]
          }
        ]
      },
      {
        sourceValue =
          contracts.Reference
          & {
            kind = "pulumi/secret",
            type = "str",
            path = "cluster.kubernetes.network.cilium.hubble-server-certs.ca.crt",
          },
        targets = [
          {
            select = { name = "hubble-server-certs", kind = "Secret" },
            fieldPaths = ["data.[ca.crt]"]
          }
        ]
      },
      {
        sourceValue =
          contracts.Reference
          & {
            kind = "pulumi/secret",
            type = "str",
            path = "cluster.kubernetes.network.cilium.hubble-server-certs.tls.crt",
          },
        targets = [
          {
            select = { name = "hubble-server-certs", kind = "Secret" },
            fieldPaths = ["data.[tls.crt]"]
          }
        ]
      },
      {
        sourceValue =
          contracts.Reference
          & {
            kind = "pulumi/secret",
            type = "str",
            path = "cluster.kubernetes.network.cilium.hubble-server-certs.tls.key",
          },
        targets = [
          {
            select = { name = "hubble-server-certs", kind = "Secret" },
            fieldPaths = ["data.[tls.key]"]
          }
        ]
      },
      {
        sourceValue =
          contracts.Reference
          & {
            kind = "pulumi/secret",
            type = "str",
            path = "cluster.kubernetes.network.cilium.hubble-relay-client-certs.ca.crt",
          },
        targets = [
          {
            select = { name = "hubble-relay-client-certs", kind = "Secret" },
            fieldPaths = ["data.[ca.crt]"]
          }
        ]
      },
      {
        sourceValue =
          contracts.Reference
          & {
            kind = "pulumi/secret",
            type = "str",
            path = "cluster.kubernetes.network.cilium.hubble-relay-client-certs.tls.crt",
          },
        targets = [
          {
            select = { name = "hubble-relay-client-certs", kind = "Secret" },
            fieldPaths = ["data.[tls.crt]"]
          }
        ]
      },
      {
        sourceValue =
          contracts.Reference
          & {
            kind = "pulumi/secret",
            type = "str",
            path = "cluster.kubernetes.network.cilium.hubble-relay-client-certs.tls.key",
          },
        targets = [
          {
            select = { name = "hubble-relay-client-certs", kind = "Secret" },
            fieldPaths = ["data.[tls.key]"]
          }
        ]
      },
    ],
  },
}
