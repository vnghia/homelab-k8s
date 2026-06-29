{
  contracts = {},
  cluster.Cluster.kubernetes
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
              manifests
                | Array { _ : Dyn },
            },
        }
    },
}
