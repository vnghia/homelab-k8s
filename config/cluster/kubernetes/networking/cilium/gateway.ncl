let class_nodeipam = "cilium-nodeipam" in
{
  cluster.kubernetes.networking.gateway = {
    cilium = {
      classes = {
        "%{class_nodeipam}" = {
          spec = {
            service = {
              allocateLoadBalancerNodePorts = false,
              ipFamilyPolicy = "RequireDualStack",
              loadBalancerClass = "io.cilium/node",
              type = "LoadBalancer",
            },
          },
        },
      },
    },
    gateways = {
      "%{class_nodeipam}" = {
        class_ = class_nodeipam,
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
