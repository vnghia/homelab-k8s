let
  port_name = "dozzle",
  port_value = 8080,
in
{
  cluster.kubernetes.apps.dozzle = {
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
    deployments = {
      dozzle = {
        account = "pod-viewer",
        containers = {
          dozzle = {
            image = {
              # renovate: datasource=docker
              repo = "ghcr.io/amir20/dozzle",
              tag = "v10.6.6",
            },
            env = {
              DOZZLE_ADDR = ":%{port_value}",
              DOZZLE_MODE = "k8s",
              DOZZLE_NO_ANALYTICS = "true",
            },
            ports = {
              "%{port_name}" = {
                container_port = port_value,
              }
            },
          },
        },
      },
    },
  },
}
