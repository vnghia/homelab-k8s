{
  cluster.kubernetes = {
    # renovate: datasource=github-releases packageName=kubernetes/kubernetes
    version = "v1.37.3",
  },
}
& (import "network/network.ncl")
& (import "apps/apps.ncl")
