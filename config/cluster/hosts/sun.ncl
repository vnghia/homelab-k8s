{
  cluster = {
    bootstrap = "sun",
    hosts.sun = {
      features = {
        controlplane = true,
        worker = true,
        loadbalancer = true,
      },
    },
  }
}
