{
  cluster.kubernetes.Namespace = {
    name | String,
    spec = {
      securities
        | {
          _ : String
        }
        | default
        = {},
    },
  },
}
