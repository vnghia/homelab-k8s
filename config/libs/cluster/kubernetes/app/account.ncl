{
  cluster.kubernetes.app.Account = {
    cluster | Bool,
    rules
      | Array {
        api_groups | Array String,
        resources | Array String,
        verbs | Array String,
      },
  },
}
