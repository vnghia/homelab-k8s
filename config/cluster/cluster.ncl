let { ClusterSchema, .. } = import "../libs/cluster.ncl" in
(import "hosts/hosts.ncl") | { cluster | ClusterSchema }
