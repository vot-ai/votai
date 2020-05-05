import Koa from 'koa'
import Router from '@koa/router'
import protect from '../middlewares/protect'

const user = new Router()

// User data
user.get('/', protect(), (ctx: Koa.Context) => {
  ctx.status = 200
  ctx.body = ctx.state.user
})

export default user
