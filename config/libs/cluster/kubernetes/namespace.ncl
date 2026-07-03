{
  cluster.kubernetes.Namespace = {
    securities
      | {
        _ : String
      }
      | default
      = {},
  },
}
