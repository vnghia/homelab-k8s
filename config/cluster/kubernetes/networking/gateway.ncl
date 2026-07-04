{
  cluster.kubernetes.networking.gateway = {
    crd = {
      # renovate: datasource=github-releases packageName=kubernetes-sigs/gateway-api
      version = "v1.5.1",
      type = "experimental",
    },
    namespace = {
      name = "gateway",
    },
  },
}
