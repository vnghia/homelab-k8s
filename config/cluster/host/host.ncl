{
  cluster.host = {
    # renovate: datasource=github-releases depName=talos packageName=siderolabs/talos
    version = "v1.13.5",
  },
}
& (import "images.ncl")
& (import "machines/machines.ncl")
