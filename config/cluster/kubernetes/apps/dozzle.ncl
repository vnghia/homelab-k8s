let
  account_name = "pod-viewer",
  deployment_name = "dozzle",
  container_name = "dozzle",
  port_name = "dozzle",
  port_value = 8080,
  service_name = "dozzle",
in
{
  cluster.kubernetes.apps.apps.dozzle = {
    accounts = {
      "%{account_name}" = {
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
      "%{deployment_name}" = {
        account = account_name,
        resources = {
          requests = {
            cpu = "0.025",
            memory = "64Mi",
          },
          limits = {
            cpu = "0.05",
            memory = "128Mi",
          },
        },
        containers = {
          "%{container_name}" = {
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
    services = {
      "%{service_name}" = {
        deployment = deployment_name,
        ports = {
          "%{port_name}" = {
            container = {
              container = container_name,
              port = port_name,
            }
          },
        },
      },
    },
  },
}
