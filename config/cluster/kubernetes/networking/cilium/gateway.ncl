let class = "cilium-nodeipam" in
{
  cluster.kubernetes.networking.gateway = {
    cilium = {
      classes = {
        "%{class}" = {
          spec = {
            service = {
              ipFamilyPolicy = "RequireDualStack",
              loadBalancerClass = "io.cilium/node",
              type = "LoadBalancer",
            },
          },
        },
      },
    },
    gateways = {
      cilium = {
        class_ = class,
        listeners = {
          https = {
            protocol = "HTTPS",
            port = 443,
          },
        },
      },
    },
  },
}
