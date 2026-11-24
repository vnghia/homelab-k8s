{
  cluster.host = {
    # renovate: datasource=github-releases packageName=siderolabs/talos
    version = "v1.14.7",
  },
}
& (import "images.ncl")
& (import "machines/machines.ncl")
