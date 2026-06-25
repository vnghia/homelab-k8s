{

  ClusterSchema = {
    name | String | default = "homelab",
    endpoint | String,
    version
      | {
        talos | String,
        k8s | String,
      },
    images
      | {
        _ : {
          extensions | Array String | default = [],
        }
      }
      | default
      = {
        default = {
          extensions = ["tailscale"],
        },
      },
    hosts
      | {
        _ : {
          endpoint | String,
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
            },
          stage
            | std.enum.TagOrString
            | [| 'initial, 'ready |],
        }
      },
  },
}
