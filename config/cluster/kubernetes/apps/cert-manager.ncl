{
  cluster.kubernetes.apps.cert_manager = {
    namespace = {
      name = "cert-manager",
    },
    chart = "oci://quay.io/jetstack/charts/cert-manager",
    # renovate: datasource=github-releases packageName=cert-manager/cert-manager
    version = "v1.20.3",
    issuer = "letsencrypt",
    secrets = {
      "%{issuer}-token" = {
        type = "Opaque",
        string_data = {
          "api-token" = {
            kind = "dns/token",
            type = "str",
            path = "cert-manager",
          },
        },
      },
    },
  },
}
