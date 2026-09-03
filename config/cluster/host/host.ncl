{
  cluster.host = {
    # renovate: datasource=github-releases packageName=siderolabs/talos
    version = "v1.14.0",
  },
}
& (import "images.ncl")
& (import "machines/machines.ncl")
