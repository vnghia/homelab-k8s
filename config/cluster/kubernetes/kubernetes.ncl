{
  cluster.kubernetes = {
    # renovate: datasource=github-releases packageName=kubernetes/kubernetes
    version = "v1.36.2",
  },
}
& (import "networking/networking.ncl")
