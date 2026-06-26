let { Nullable, .. } = import "contracts.ncl" in
{
  ClusterHostMachineProvisioningVolumeSchema = {
    selector | String,
    min_size | Nullable String | default = null,
    max_size | Nullable String | default = null,
  },

  ClusterSchema = {
    name | String,
    domain
      | {
        prefix | Nullable String,
        name | String,
      },
    version
      | {
        talos | String,
        k8s | String,
      },
    host
      | {
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
                        | ClusterHostMachineProvisioningVolumeSchema
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
  },
}
