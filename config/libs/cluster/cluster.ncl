{
  contracts = {},
  cluster.Cluster = {
    stack | String | not_exported,
  }
}
& (import "kubernetes/kubernetes.ncl")
& (import "host/host.ncl")
