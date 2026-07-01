{
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
            namespace | String,
            chart | String,
            version | String,
          },
      },
  },
}
