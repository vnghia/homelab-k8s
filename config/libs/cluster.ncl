let versions = import "../versions/cluster.yaml" in
{
  ImageSchema = {
    extensions | Array String | default = [],
  },

  HostSchema = {
    address | String,
    image | ImageSchema | default = {},
  },

  CluserSchema = {
    name | String | default = "homelab",
    version = versions.github.cluster.release,
    endpoint | String = "sun",
    hosts | { _ : HostSchema },
  },

  common_extensions = ["tailscale"],
}
