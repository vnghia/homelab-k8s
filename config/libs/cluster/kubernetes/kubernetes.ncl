(import "namespace.ncl")
& (import "custom-resource.ncl")
& (import "app/app.ncl")
& {
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
                kustomization | { _ : Dyn },
              },
            certificate
              | cluster.kubernetes.App
              & {
                issuer | String,
                email | String | not_exported,
              },
            policy
              | {
                cluster | { _ : Dyn },
              },
          },
        apps
          | {
            _ : cluster.kubernetes.App
          },
      },
  },
}
