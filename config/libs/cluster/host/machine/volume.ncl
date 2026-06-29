{
  contracts = {},
  cluster.host.machine.volume = {
    Provisioning = {
      selector | String,
      min_size | contracts.Nullable String | default = null,
      max_size | contracts.Nullable String | default = null,
    },
  },
}
