{
  contracts = {},
  cluster = {
    kubernetes.Kustomization = import "kustomization.ncl",
    Cluster.kubernetes
      | {
        version | String,
        domain
          | {
            prefix | contracts.Nullable String,
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
                version | String,
                kustomization | cluster.kubernetes.Kustomization,
              },
          }
      },
  },
}
