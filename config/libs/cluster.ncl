{
  VersionSchema = {
    talos | String,
    k8s | String,
  },

  ImageSchema = {
    extensions | Array String | default = [],
  },

  HostSchema = {
    image | String | default = "default",
    address | String,
  },

  ClusterSchema = {
    name | String | default = "homelab",
    version | VersionSchema,
    endpoint | String,
    images | { _ : ImageSchema } | default = {
      default = {
        extensions = ["tailscale"],
      },
    },
    hosts | { _ : HostSchema },
  },
}
