{
  contracts = {},
  cluster.kubernetes.app.Chart = {
    chart | String,
    version | String,
    skip_crds | Bool,
    repository
      | contracts.Nullable {
        repo | String,
      }
      | default
      = null,
    values | { _ : Dyn },
  },
}
