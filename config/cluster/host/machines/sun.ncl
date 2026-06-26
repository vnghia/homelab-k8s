{
  cluster.host = {
    bootstrap = "sun",
    machines.sun = {
      features = {
        controlplane = true,
        worker = true,
        loadbalancer = true,
      },
    },
  }
}
