{
  ImageSchema = {
    version | String,
    extensions | Array String | default = [],
  },

  Schema = {
    address | String,
    image | ImageSchema,
  },
}
