{
  cluster.kubernetes.network.gateway = {
    crd = {
      # renovate: datasource=github-releases packageName=kubernetes-sigs/gateway-api
      version = "v1.6.3",
      type = "standard",
    },
    namespace = {
      name = "gateway",
    },
  },
}
