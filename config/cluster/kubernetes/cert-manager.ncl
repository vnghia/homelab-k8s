{
  cluster.kubernetes.cert_manager = {
    namespace = "cert-manager",
    chart = "oci://quay.io/jetstack/charts/cert-manager",
    # renovate: datasource=helm packageName=oci://quay.io/jetstack/charts/cert-manager
    version = "v1.20.3",
  },
}
