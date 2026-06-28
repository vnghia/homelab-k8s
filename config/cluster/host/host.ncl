{
  cluster.host = {
    # renovate: datasource=github-releases packageName=siderolabs/talos
    version = "v1.13.5",
  },
}
& (import "images.ncl")
& (import "machines/machines.ncl")
