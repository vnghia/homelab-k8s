{
  cluster.kubernetes.services.dozzle = {
    accounts = {
      pod-viewer = {
        cluster = true,
        rules = [
          {
            api_groups = [""],
            resources = ["pods", "pods/log", "nodes"],
            verbs = ["get", "list", "watch"],
          },
          {
            api_groups = ["apps"],
            resources = ["deployments", "replicasets", "daemonsets", "statefulsets"],
            verbs = ["get"],
          },
          {
            api_groups = ["batch"],
            resources = ["jobs", "cronjobs"],
            verbs = ["get"],
          },
          {
            api_groups = ["metrics.k8s.io"],
            resources = ["pods"],
            verbs = ["get", "list"],
          }
        ],
      }
    },
  },
}
