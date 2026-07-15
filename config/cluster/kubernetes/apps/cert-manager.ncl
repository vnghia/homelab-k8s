let { contracts, .. } = import "../../../libs/contracts.ncl" in
{
  cluster.kubernetes.apps.cert_manager =
    let issuer = cluster.kubernetes.apps.cert_manager.issuer in
    let
      secret_name = "%{issuer}-token",
      secret_key = "%{issuer}-token",
    in
    {
      namespace = {
        name = "cert-manager",
      },

      chart = "oci://quay.io/jetstack/charts/cert-manager",
      # renovate: datasource=github-releases packageName=cert-manager/cert-manager
      version = "v1.20.3",

      issuer = "letsencrypt",

      secrets = {
        "%{secret_name}" = {
          type = "Opaque",
          string_data = {
            "%{secret_key}" = {
              kind = "dns/token",
              type = "str",
              path = "cert_manager",
            },
          },
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
              email = cluster.kubernetes.apps.cert_manager.email,
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
