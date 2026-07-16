let { contracts, .. } = import "../../../libs/contracts.ncl" in
{
  cluster.kubernetes.networking.certificate =
    let rec
      issuer = cluster.kubernetes.networking.certificate.issuer,
      secret_name = "%{issuer}-token",
      secret_key = "%{issuer}-token",
    in
    {
      issuer = "letsencrypt",
      namespace = {
        name = "certificate",
      },
      secrets = {
        "%{secret_name}" = {
          type = "Opaque",
          string_data = {
            "%{secret_key}" = {
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
          version = "v1.20.3",
          skip_crds = false,
          values = {
            crds = {
              enabled = true,
            },
            config = {
              enableGatewayAPI = true,
              enableGatewayAPIListenerSet = true,
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
              server =
                if cluster.stack != null then
                  "https://acme-staging-v02.api.letsencrypt.org/directory"
                else
                  "https://acme-v02.api.letsencrypt.org/directory",
              email = cluster.kubernetes.networking.certificate.email,
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
                            path = "secrets.%{secret_name}.name",
                          },
                        key = secret_key,
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
