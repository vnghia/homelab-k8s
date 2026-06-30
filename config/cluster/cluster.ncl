let
  libs = import "../libs/libs.ncl",
  kubernetes = import "kubernetes/kubernetes.ncl",
  host = import "host/host.ncl",
in
{
  cluster | libs.cluster.Cluster
}
& kubernetes
& host
