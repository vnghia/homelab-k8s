{
  contracts = {
    Nullable = fun Contract =>
      std.contract.custom (fun label value =>
        if value == null then
          'Ok value
        else
          std.contract.check Contract label value
      ),

    Reference = {
      kind | String,
      type
        | std.enum.TagOrString
        | [| 'str, 'bool, 'int, 'float |],
      path | String,
    },

    kubernetes = {
      AppReference =
        Reference
        & {
          kind = "kubernetes/app",
          name | Nullable String | default = null,
        },
    },
  },
}
