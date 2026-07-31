let { contracts, .. } = import "../../../libs/contracts.ncl"
in
{
  cluster.kubernetes.network.certificate =
    let rec
      manager_label = {
        "%{cluster.kubernetes.label.app}/part-of" = "manager",
      },

      # issuer
      acme_endpoint =
        if cluster.stack != null then
          "acme-staging-v02.api.letsencrypt.org"
        else
          "acme-v02.api.letsencrypt.org",
      issuer = cluster.kubernetes.network.certificate.issuer,
      issuer_secret_name = "%{issuer}-token",
      issuer_secret_key = "%{issuer}-token",
    in
    {
      issuer = "letsencrypt",
      namespace = {
        name = "certificate",
      },
      network = {
        policies = {
          manager = {
            endpointSelector = {
              matchLabels = manager_label,
            },
            egress = [
              {
                toEntities = [
                  "kube-apiserver"
                ],
                toPorts = [
                  {
                    ports = [
                      {
                        port = "6443",
                        protocol = "TCP",
                      },
                    ],
                  },
                ],
              },
              {
                toFQDNs = [
                  {
                    matchName = acme_endpoint,
                  },
                ],
                toPorts = [
                  {
                    ports = [
                      {
                        port = "443",
                        protocol = "TCP",
                      },
                    ],
                  },
                ],
              }
            ],
          },
        },
      },
      secrets = {
        "%{issuer_secret_name}" = {
          type = "Opaque",
          string_data = {
            "%{issuer_secret_key}" = {
              kind = "dns/token",
              type = "str",
              path = issuer,
            },
          },
        },
      },
      charts = {
        manager = {
          chart = "oci://quay.io/jetstack/charts/cert-manager",
          # renovate: datasource=github-releases packageName=cert-manager/cert-manager
          version = "v1.21.1",
          skip_crds = false,
          values = {
            crds = {
              enabled = true,
            },
            global = {
              commonLabels = manager_label,
            },
            nameOverride = cluster.kubernetes.network.certificate.namespace.name,
            config = {
              gatewayAPI = {
                enabled = true,
                enableListenerSet = true,
              },
              featureGates = {
                ListenerSets = true,
              },
            },
          }
        },
      },
      custom_resources = {
        "%{issuer}" = {
          api_version = "cert-manager.io/v1",
          kind = "ClusterIssuer",
          spec = {
            acme = {
              server = "https://%{acme_endpoint}/directory",
              email = cluster.kubernetes.network.certificate.email,
              privateKeySecretRef = {
                name = "%{issuer}-account-key",
              },
              solvers = [
                {
                  dns01 = {
                    cloudflare = {
                      apiTokenSecretRef = {
                        name =
                          contracts.kubernetes.AppReference
                          & {
                            type = "str",
                            path = "secrets.%{issuer_secret_name}.name",
                          },
                        key = issuer_secret_key,
                      },
                    },
                  },
                },
              ],
            },
          },
        },
      },
    },
}
