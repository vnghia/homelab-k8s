{
  cluster.kubernetes.networking.policy = {
    cluster = {
      intercept-all-dns = {
        endpointSelector = {
          matchExpressions = [
            {
              key = "io.kubernetes.pod.namespace",
              operator = "NotIn",
              values = [
                "kube-system",
                "cilium-core",
              ],
            },
            {
              key = "k8s-app",
              operator = "NotIn",
              values = [
                "kube-dns"
              ],
            },
          ],
        },
        enableDefaultDeny = {
          egress = true,
          ingress = true,
        },
        egress = [
          {
            toEndpoints = [
              {
                matchLabels = {
                  "io.kubernetes.pod.namespace" = "kube-system",
                  "k8s-app" = "kube-dns"
                },
              },
            ],
            toPorts = [
              {
                ports = [
                  {
                    port = "53",
                    protocol = "TCP",
                  },
                  {
                    port = "53",
                    protocol = "UDP",
                  },
                ],
                rules = {
                  dns = [
                    {
                      matchPattern = "*"
                    },
                  ],
                },
              },
            ],
          },
        ],
      },
    },
  },
}
