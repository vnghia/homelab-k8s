let
  lib = import "../libs/cluster.ncl",
  kubernetes = import "kubernetes/kubernetes.ncl",
  host = import "host/host.ncl",
in
{
  cluster | lib.ClusterSchema = {
    name = "homelab",
  }
}
& kubernetes
& host
