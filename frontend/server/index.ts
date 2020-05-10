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

// Middlewares
import { errorMiddleware } from './middlewares/error'
import { authenticationMiddleware } from './middlewares/auth'

mongoose.connect(mongoConnectionString)
mongoose.connection.on('error', consola.error)
mongoose.connection.on('connected', () =>
  consola.success('Connected to mongo!')
)

const router = new Router()
// API Routes
router.use('/api', api.routes(), api.allowedMethods())

// Create Koa App
const app = new Koa()

// Setup middlewares
app.use(errorMiddleware())
app.use(async (ctx: Koa.Context, next: Koa.Next) => {
  // Disable body parser if the request was not to the API
  if (!ctx.url.startsWith('/api')) {
    ctx.disableBodyParser = true
  }
  await next()
})
app.use(bodyParser())
app.use(
  logger((str, args) => {
    const arrArgs = args as string[]
    const [, , url, , ,] = arrArgs
    if (!['/_nuxt', '/__', '/sw.js', '/vuetify'].some(s => url.startsWith(s))) {
      consola.log(str)
    }
  })
)
app.use(helmet())
app.use(authenticationMiddleware())

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
