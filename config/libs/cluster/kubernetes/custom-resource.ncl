{
  cluster.kubernetes.CustomResource = {
    api_version | String,
    kind | String,
    spec | { _ : Dyn },
  },
}
