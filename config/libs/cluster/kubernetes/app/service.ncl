{
  contracts = {},
  cluster.kubernetes.app.Service = {
    deployment | String,
    ports
      | {
        _ : {
          port | contracts.Nullable Number | default = null,
          container
            | {
              container | String,
              port | String,
            },
        }
      },
  },
}
