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
    version = versions.github.cluster.release,
    hosts | { _ : HostSchema },
  },

  common_extensions = ["tailscale"],
}
