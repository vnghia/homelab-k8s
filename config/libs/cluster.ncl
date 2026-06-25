let versions = import "../versions/cluster.yaml" in
{
  ImageSchema = {
    extensions | Array String | default = [],
  },

  HostSchema = {
    image | String | default = "default",
    address | String,
  },

  ClusterSchema = {
    name | String | default = "homelab",
    version = versions.github.cluster.release,
    entrypoint | String | not_exported,
    endpoint | String = "https://%{hosts."%{entrypoint}".address}:6443",
    images | { _ : ImageSchema } | default = {
      default = {
        extensions = ["tailscale"],
      },
    },
    hosts | { _ : HostSchema },
  },
}
