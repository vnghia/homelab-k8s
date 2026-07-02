(import "container.ncl")
& {
  contracts = {},
  cluster.kubernetes.service.Deployment = {
    account | contracts.Nullable String | default = null,
    containers
      | {
        _ : cluster.kubernetes.service.deployment.Container
      },
  },
}
