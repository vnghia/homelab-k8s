(import "namespace.ncl")
& (import "service/service.ncl")
& {
  contracts = {},
  cluster = {
    kubernetes.Kustomization = import "kustomization.ncl",
    Cluster.kubernetes
      | {
        version | String,
        domain
          | {
            cluster | String,
            name | String,
          },
        networking
          | {
            gateway
              | {
                version | String,
                type
                  | std.enum.TagOrString
                  | [| 'standard, 'experimental |],
              },
            cilium
              | {
                namespace | String,
                version | String | not_exported,
                kustomization | cluster.kubernetes.Kustomization,
              },
          },
        cert_manager
          | {
            namespace
              | {
                name | String,
                config | cluster.kubernetes.Namespace | default = {},
              },
            chart | String,
            version | String,
            issuer | String,
            email | String,
          },
        services
          | {
            _ : cluster.kubernetes.Service
          },
      },
  },
}
