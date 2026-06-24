let versions = import "../versions/host.yaml" in
{
  ImageSchema = {
    version | String | default = versions.github.image.release,
    extensions | Array String | default = [],
  },

  Schema = {
    address | String,
    image | ImageSchema = {},
  },

  common_extensions = ["tailscale"],
}
