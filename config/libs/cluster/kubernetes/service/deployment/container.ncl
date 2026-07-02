{
  cluster.kubernetes.service.deployment.Container = {
    image
      | {
        repo | String,
        tag | String,
      },
    env
      | {
        _ : String
      },
  },
}
