(import "account.ncl")
& (import "deployment/deployment.ncl")
& (import "secret.ncl")
& (import "service.ncl")
& {
  contracts = {},
  cluster.kubernetes.App = {
    namespace
      | cluster.kubernetes.Namespace
      & {
        name | default = "",
        spec = {
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
    secrets
      | {
        _ : cluster.kubernetes.app.Secret
      }
      | default
      = {},
    deployments
      | {
        _ : cluster.kubernetes.app.Deployment
      }
      | default
      = {},
    services
      | {
        _ : cluster.kubernetes.app.Service
      }
      | default
      = {},
  },
}
