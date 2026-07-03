(import "account.ncl")
& (import "deployment/deployment.ncl")
& {
  contracts = {},
  cluster.kubernetes.App = {
    namespace
      | {
        name | contracts.Nullable String | default = null,
        config | cluster.kubernetes.Namespace = {
          securities = {
            enforce | default = "restricted",
            audit | default = "restricted",
            warn | default = "restricted",
          }
        },
      }
      | default
      = {},
    accounts
      | {
        _ : cluster.kubernetes.app.Account
      }
      | default
      = {},
    deployments
      | {
        _ : cluster.kubernetes.app.Deployment
      },
  },
}
