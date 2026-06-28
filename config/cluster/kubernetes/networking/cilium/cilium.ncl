{
  cluster.kubernetes.networking.cilium = {
    namespace = "cilium-core",
  },
}
& (import "manifests.ncl")
