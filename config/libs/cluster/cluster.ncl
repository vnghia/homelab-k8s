{
  contracts = {},
  cluster.Cluster = {
    name | String,
  }
}
& (import "kubernetes/kubernetes.ncl")
& (import "host/host.ncl")
