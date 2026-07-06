{
  cluster.kubernetes.app.deployment.Container = {
    image
      | {
        repo | String,
        tag | String,
      },
    env
      | {
        _ : String
      },
    ports
      | {
        _ : {
          container_port | Number,
        }
      },
    resources
      | {
        requests | { _ : String } | default = {},
        limits | { _ : String } | default = {},
      }
      | default
      = {},
    security_context
      | {
        allow_privilege_escalation | Bool | default = false,
        capabilities
          | {
            add | Array String | default = [],
            drop | Array String | default = ["ALL"],
          }
          | default
          = {},
        privileged | Bool | default = false,
        read_only_root_filesystem | Bool | default = true,
        run_as_group | Number | default = 1000,
        run_as_non_root | Bool | default = true,
        run_as_user | Number | default = 1000,
        seccomp_profile
          | {
            type | String | default = "RuntimeDefault",
          }
          | default
          = {},
      }
      | default
      = {},
  },
}
