let cluster = import "../libs/cluster.ncl" in
{
  hosts = import "hosts/hosts.ncl",
} | cluster.CluserSchema
