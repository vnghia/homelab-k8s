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
                namespace | cluster.kubernetes.Namespace,
                cilium
                  | {
                    classes
                      | {
                        _ : {
                          spec
                            | {
                              _ : Dyn
                            }
                        }
                      }
                  },
                gateways
                  | {
                    _ : {
                      class_ | String,
                      listeners
                        | {
                          _ : {
                            protocol | String,
                            port | Number,
                          }
                        },
                    }
                  },
              },
            cilium
              | {
                namespace | cluster.kubernetes.Namespace,
                version | String | not_exported,
                kustomization | cluster.kubernetes.Kustomization,
              },
          },
        apps
          | {
            cert_manager
              | cluster.kubernetes.App
              & {
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
  },
}
