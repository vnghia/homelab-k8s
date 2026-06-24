let host = import "../libs/host.ncl" in
{
  image = { extensions = host.common_extensions }
} | host.Schema
