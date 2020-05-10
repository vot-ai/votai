import Router from '@koa/router'
import { authenticationRequired } from '../middlewares/protect'
import { ResponseStatus } from '../types/responses'
import { ContextWithState, AuthenticatedUserState } from '../types/context'
import { isRegistered } from '../middlewares/auth'
import SurveyController from '../controllers/surveys'

const user = new Router()

// User data
user.get(
  '/',
  authenticationRequired(),
  async (ctx: ContextWithState<AuthenticatedUserState>) => {
    const user = ctx.state.user
    await SurveyController.create(ctx)
    const response = isRegistered(user) ? user.serialize() : user.serialize()
    ctx.body = response
    ctx.status = ResponseStatus.OK
  }
)

export default user
