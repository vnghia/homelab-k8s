{
  cluster.kubernetes.networking.cilium = {
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
    version = "1.19.5",
  },
}
& (import "kustomization.ncl")
