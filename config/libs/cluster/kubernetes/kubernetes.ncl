(import "namespace.ncl")
& (import "app/app.ncl")
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
                crd
                  | {
                    version | String,
                    type
                      | std.enum.TagOrString
                      | [| 'standard, 'experimental |],
                  },
              },
            cilium
              | {
                namespace | cluster.kubernetes.Namespace,
                version | String | not_exported,
                kustomization | cluster.kubernetes.Kustomization,
              },
          },
        cert_manager
          | {
            namespace | cluster.kubernetes.Namespace,
            chart | String,
            version | String,
            issuer | String,
            email | String,
          },
        apps
          | {
            _ : cluster.kubernetes.App
          },
      },
  },
}
