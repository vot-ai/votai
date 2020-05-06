// @ts-ignore
export default ({ app }) => {
  // @ts-ignore
  app.$auth.onRedirect(to => {
    return app.localePath(to)
  })
}
