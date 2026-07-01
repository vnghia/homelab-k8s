let libs = import "../libs/libs.ncl",
in
{
  dns | libs.dns.Dns = {
    zones = {
      cluster = {},
    },
  },
}
