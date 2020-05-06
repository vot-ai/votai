import Koa from 'koa'
import Router from '@koa/router'
import protect from '../middlewares/protect'
import { SerializedUser } from '../models/user'
import { ResponseStatus, ResponseMessages } from '../types/responses'
import UserController from '../controllers/users'

const user = new Router()

// User data
user.get('/', protect(), async (ctx: Koa.Context) => {
  const serialized: SerializedUser = ctx.state.user
  const user = await UserController.findUserByEmail(serialized)
  if (user) {
    ctx.body = user.serialize()
    ctx.status = ResponseStatus.OK
  } else {
    ctx.body = ResponseMessages.UNAUTHORIZED_ERROR
    ctx.status = ResponseStatus.UNAUTHORIZED_ERROR
  }
})

export default user
