{
  cluster.kubernetes.networking.cilium = {
    namespace = "cilium-core",
    # renovate: datasource=github-releases packageName=cilium/cilium
    version = "1.19.5",
  },
}
& (import "kustomization.ncl")
