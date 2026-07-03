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
            networking
              | {
                interfaces
                  | {
                    _ : {
                      dhcpv4 | Bool | default = true,
                      dhcpv6 | Bool | default = true,
                    }
                  },
                cluster
                  | {
                    pod_subnets | Array String,
                    service_subnets | Array String,
                  }
              },
            stage
              | std.enum.TagOrString
              | [| 'initial, 'ready |],
          }
        },
    },
}
