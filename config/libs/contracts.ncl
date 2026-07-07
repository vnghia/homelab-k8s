{
  contracts = {
    Nullable = fun Contract =>
      std.contract.custom (fun label value =>
        if value == null then
          'Ok value
        else
          std.contract.check Contract label value
      ),

    reference = {
      pulumi = {
        Secret = {
          kind = "pulumi/secret",
          type
            | std.enum.TagOrString
            | [| 'str, 'bool, 'int, 'float |],
          path | String,
        },
      },
    },
  },
}
