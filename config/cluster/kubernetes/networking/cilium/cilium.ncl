{
  cluster.kubernetes.networking.cilium = {
    namespace = "cilium-core",
    # renovate: datasource=helm packageName=cilium
    version = "1.19.5",
  },
}
& (import "kustomization.ncl")
