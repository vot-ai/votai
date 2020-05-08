import Router from '@koa/router'
import { authenticationRequired } from '../middlewares/protect'
import { ResponseStatus } from '../types/responses'
import { ContextWithState, AuthenticatedUserState } from '../types/context'
import { isRegistered } from '../middlewares/auth'

const user = new Router()

// User data
user.get(
  '/',
  authenticationRequired(),
  (ctx: ContextWithState<AuthenticatedUserState>) => {
    const user = ctx.state.user
    const response = isRegistered(user) ? user.serialize() : user.serialize()
    ctx.body = response
    ctx.status = ResponseStatus.OK
  }
)

export default user
