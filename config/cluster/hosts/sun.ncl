let cluster = import "../../libs/cluster.ncl" in
{
  image = { extensions = cluster.common_extensions }
} | cluster.HostSchema
