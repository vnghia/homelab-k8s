{
  VersionSchema = {
    talos | String,
    k8s | String,
  },

  ImageSchema = {
    extensions | Array String | default = [],
  },

  HostSchema = {
    endpoint | String,
    controlplane | Bool,
    worker | Bool,
    install
      | {
        disk | String,
        image | String | default = "default",
      },
  },

  ClusterSchema = {
    name | String | default = "homelab",
    endpoint | String,
    version | VersionSchema,
    images | { _ : ImageSchema } | default = {
      default = {
        extensions = ["tailscale"],
      },
    },
    hosts | { _ : HostSchema },
  },
}
