(import "container.ncl")
& {
  contracts = {},
  cluster.kubernetes.app.Deployment = {
    account | contracts.Nullable String | default = null,
    security_context
      | {
        fs_group | Number | default = 1000,
        fs_group_change_policy
          | std.enum.TagOrString
          | [| 'Always, 'OnRootMismatch |]
          = 'OnRootMismatch,
        run_as_group | Number | default = 1000,
        run_as_non_root | Bool | default = true,
        run_as_user | Number | default = 1000,
        seccomp_profile
          | {
            type | String | default = "RuntimeDefault",
          }
          | default
          = {},
        supplemental_groups | Array Number | default = [],
        supplemental_groups_policy
          | std.enum.TagOrString
          | [| 'Merge, 'Strict |]
          = 'Merge,
      }
      | default
      = {},
    containers
      | {
        _ : cluster.kubernetes.app.deployment.Container
      },
  },
}
