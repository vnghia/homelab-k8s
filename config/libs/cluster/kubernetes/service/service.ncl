(import "account.ncl")
& {
  cluster.kubernetes.Service = {
    accounts
      | {
        _ : cluster.kubernetes.service.Account
      }
      | default
      = {},
  },
}
