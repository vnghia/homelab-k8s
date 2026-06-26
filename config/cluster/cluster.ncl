let
  cluster_lib = import "../libs/cluster.ncl",
  cluster_version = import "../versions/cluster.yaml",
  hosts = import "host/host.ncl",
in
{
  cluster | cluster_lib.ClusterSchema = {
    name = "homelab",
    version = {
      talos = cluster_version.github.talos.release,
      k8s = cluster_version.github.k8s.release,
    },
  }
}
& hosts
