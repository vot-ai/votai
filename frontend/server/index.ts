import Koa from 'koa'
import Router from '@koa/router'
import bodyParser from 'koa-bodyparser'
import logger from 'koa-logger'
import helmet from 'koa-helmet'
import mongoose from 'mongoose'
import consola from 'consola'
// @ts-ignore
import { Nuxt, Builder } from 'nuxt'
// Import and Set Nuxt.js options
import config from '../nuxt.config'

import { mongoConnectionString } from './config'

// Routes
import api from './routes'

mongoose.connect(mongoConnectionString)
mongoose.connection.on('error', consola.error)
mongoose.connection.on('connected', () =>
  consola.success('Connected to mongo!')
)

const app = new Koa()
const router = new Router()

app.use(async (ctx: Koa.Context, next: Koa.Next) => {
  if (!ctx.url.startsWith('/api')) {
    ctx.disableBodyParser = true
  }
  await next()
})
// Setup middlewares
app.use(bodyParser())
app.use(logger())
app.use(helmet())

// API Routes
router.use('/api', api.routes(), api.allowedMethods())

// Register base router
app.use(router.routes())

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
