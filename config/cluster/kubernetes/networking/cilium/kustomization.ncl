{
  cluster.kubernetes.networking.cilium.kustomization = {
    apiVersion = "kustomize.config.k8s.io/v1beta1",
    kind = "Kustomization",
    helmCharts = [
      {
        name = "cilium",
        releaseName = "cilium",
        namespace = cluster.kubernetes.networking.cilium.namespace,
        repo = "https://helm.cilium.io/",
        version = cluster.kubernetes.networking.cilium.version,
        valuesInline = {
          bpf = { hostLegacyRouting = false, masquerade = true },
          cgroup = {
            autoMount = { enabled = false },
            hostRoot = "/sys/fs/cgroup"
          },
          egressGateway = {
            enabled = true,
          },
          gatewayAPI = {
            enabled = true,
            enableAlpn = true,
            enableAppProtocol = true
          },
          hubble = {
            enabled = true,
            relay = { enabled = true },
            ui = { enabled = true },
          },
          ipam = { mode = "kubernetes" },
          kubeProxyReplacement = true,
          k8sServiceHost = "localhost",
          k8sServicePort = 7445,
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
              name = cluster.kubernetes.networking.cilium.namespace,
            },
          },
        },
      }
    ],
    replacements = [
      {
        sourceValue = "#ref:pulumi/secrets:str:cluster.kubernetes.networking.cilium.cilium-ca.ca.crt",
        targets = [
          {
            select = { name = "cilium-ca", kind = "Secret" },
            fieldPaths = ["data.[ca.crt]"]
          }
        ]
      },
      {
        sourceValue = "#ref:pulumi/secrets:str:cluster.kubernetes.networking.cilium.cilium-ca.ca.key",
        targets = [
          {
            select = { name = "cilium-ca", kind = "Secret" },
            fieldPaths = ["data.[ca.key]"]
          }
        ]
      },
      {
        sourceValue = "#ref:pulumi/secrets:str:cluster.kubernetes.networking.cilium.hubble-server-certs.ca.crt",
        targets = [
          {
            select = { name = "hubble-server-certs", kind = "Secret" },
            fieldPaths = ["data.[ca.crt]"]
          }
        ]
      },
      {
        sourceValue = "#ref:pulumi/secrets:str:cluster.kubernetes.networking.cilium.hubble-server-certs.tls.crt",
        targets = [
          {
            select = { name = "hubble-server-certs", kind = "Secret" },
            fieldPaths = ["data.[tls.crt]"]
          }
        ]
      },
      {
        sourceValue = "#ref:pulumi/secrets:str:cluster.kubernetes.networking.cilium.hubble-server-certs.tls.key",
        targets = [
          {
            select = { name = "hubble-server-certs", kind = "Secret" },
            fieldPaths = ["data.[tls.key]"]
          }
        ]
      },
      {
        sourceValue = "#ref:pulumi/secrets:str:cluster.kubernetes.networking.cilium.hubble-relay-client-certs.ca.crt",
        targets = [
          {
            select = { name = "hubble-relay-client-certs", kind = "Secret" },
            fieldPaths = ["data.[ca.crt]"]
          }
        ]
      },
      {
        sourceValue = "#ref:pulumi/secrets:str:cluster.kubernetes.networking.cilium.hubble-relay-client-certs.tls.crt",
        targets = [
          {
            select = { name = "hubble-relay-client-certs", kind = "Secret" },
            fieldPaths = ["data.[tls.crt]"]
          }
        ]
      },
      {
        sourceValue = "#ref:pulumi/secrets:str:cluster.kubernetes.networking.cilium.hubble-relay-client-certs.tls.key",
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
