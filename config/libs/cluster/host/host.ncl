(import "machine/machine.ncl")
& {
  cluster.Cluster.host
    | {
      version | String,
      bootstrap | String,
      images
        | {
          _ : {
            extensions | Array String | default = [],
          }
        },
      machines
        | {
          _ : {
            ips
              | {
                tailscale : String,
              },
            features
              | {
                controlplane | Bool,
                worker | Bool,
                loadbalancer | Bool,
              },
            install
              | {
                disk | String,
                image | String | default = "default",
                volumes
                  | {
                    ephemeral
                      | cluster.host.machine.volume.Provisioning
                      & {
                        selector | String | default = "system_disk",
                      }
                      | default
                      = {},
                  }
                  | default
                  = {},
              },
            stage
              | std.enum.TagOrString
              | [| 'initial, 'ready |],
          }
        },
    },
}
