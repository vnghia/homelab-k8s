{
  cluster.kubernetes.app.CustomResource = {
    cluster | Bool | default = false,
    api_version | String,
    kind | String,
    spec | { _ : Dyn },
  },
}
