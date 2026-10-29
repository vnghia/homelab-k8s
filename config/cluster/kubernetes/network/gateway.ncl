{
  cluster.kubernetes.network.gateway = {
    crd = {
      # renovate: datasource=github-releases packageName=kubernetes-sigs/gateway-api
      version = "v1.7.0",
      type = "standard",
    },
    namespace = {
      name = "gateway",
    },
  },
}
