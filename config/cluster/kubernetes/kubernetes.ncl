{
  cluster.kubernetes = {
    # renovate: datasource=github-releases packageName=kubernetes/kubernetes
    version = "v1.36.2",
    networking = {
      gateway = {
        # renovate: datasource=github-releases packageName=kubernetes-sigs/gateway-api
        version = "v1.5.1",
        type = "experimental",
      },
    },
  },
}
