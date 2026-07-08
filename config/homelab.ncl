let { contracts, .. } = import "libs/contracts.ncl" in
{ stack | contracts.Nullable String | not_exported } & (import "dns/dns.ncl") & (import "cluster/cluster.ncl")
