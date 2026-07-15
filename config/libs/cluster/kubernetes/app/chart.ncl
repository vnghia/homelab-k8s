{
  cluster.kubernetes.app.Chart = {
    chart | String,
    version | String,
    skip_crds | Bool,
    values | { _ : Dyn },
  },
}
