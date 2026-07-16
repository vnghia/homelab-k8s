let { contracts, .. } = import "../../../libs/contracts.ncl" in
{
  cluster.kubernetes.apps.metrics-server = {
    namespace = {
      name = "metrics-server",
    },
    charts = {
      metrics-server = {
        chart = "metrics-server",
        version = "v3.13.1",
        skip_crds = false,
        repository = {
          repo = "https://kubernetes-sigs.github.io/metrics-server",
        },
        values = {
          args = [
            # This is necessary because Talos uses self-signed kubelet certs
            "--kubelet-insecure-tls",
            # Use InternalIP to connect to nodes (avoids hostname resolution issues)
            "--kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname",
            # Metric resolution interval
            "--metric-resolution=15s",
          ],
          apiService = {
            insecureSkipTLSVerify = false,
          },
          tls = {
            type = "helm",
          },
        }
      },
    },
  }
}
