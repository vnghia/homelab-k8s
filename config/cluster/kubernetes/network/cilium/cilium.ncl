{
  cluster.kubernetes.network.cilium = {
    namespace = {
      name = "cilium-core",
      spec = {
        securities = {
          audit = "privileged",
          enforce = "privileged",
          warn = "privileged",
        },
      },
    },
    # renovate: datasource=github-releases packageName=cilium/cilium
    version = "1.20.0",
  },
}
& (import "kustomization.ncl")
& (import "gateway.ncl")
