(import "account.ncl")
& (import "deployment/deployment.ncl")
& {
  cluster.kubernetes.Service = {
    accounts
      | {
        _ : cluster.kubernetes.service.Account
      }
      | default
      = {},
    deployments
      | {
        _ : cluster.kubernetes.service.Deployment
      },
  },
}
