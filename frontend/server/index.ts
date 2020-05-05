import Koa from 'koa'
import consola from 'consola'
// @ts-ignore
import { Nuxt, Builder } from 'nuxt'

import bodyParser from 'koa-bodyparser'
import logger from 'koa-logger'
import helmet from 'koa-helmet'

// Import and Set Nuxt.js options
import config from "../nuxt.config"

const app = new Koa()

// Setup middlewares
app.use(bodyParser())
app.use(logger())
app.use(helmet())

// Configure Koa middlewares

config.dev = app.env !== 'production'

async function start() {
  // Instantiate nuxt.js
  const nuxt = new Nuxt(config)

  const {
    host = process.env.HOST || '0.0.0.0',
    port = process.env.PORT || 3000
  } = nuxt.options.server

  await nuxt.ready()


  // Build in development
  if (config.dev) {
    const builder = new Builder(nuxt)
    await builder.build()
  }

  app.use((ctx: Koa.Context) => {
    ctx.status = 200
    ctx.respond = false // Bypass Koa's built-in response handling
    // @ts-ignore
    ctx.req.ctx = ctx // This might be useful later on, e.g. in nuxtServerInit or with nuxt-stash
    nuxt.render(ctx.req, ctx.res)
  })

  app.listen(port, host)
  consola.ready({
    message: `Server listening on http://${host}:${port}`,
    badge: true
  })
}

start()
