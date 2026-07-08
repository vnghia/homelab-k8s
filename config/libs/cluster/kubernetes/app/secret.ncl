{
  cluster.kubernetes.app.Secret = {
    type | String,
    string_data | { _ : Dyn } | default = {},
  },
}
