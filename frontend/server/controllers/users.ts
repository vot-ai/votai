import { Next } from 'koa'
import User from '../models/user'
import {
  ContextWithState,
  UserDataState,
  MaybeUserState
} from '../types/context'
import { ResponseMessages, ResponseStatus } from '../types/responses'

class UserController {
  private create = async (ctx: ContextWithState<UserDataState>, next: Next) => {
    const userData = ctx.state.userData
    const { provider, profileData, ...user } = userData
    const newUserBody = {
      ...user,
      identities: [{ provider, userId: user.userId, profileData }]
    }
    const newUser = await User.create(newUserBody).catch(() => null)

    if (newUser) {
      // Set the current user and go to next middleware
      ctx.state.user = newUser
      await next()
    } else {
      ctx.status = ResponseStatus.VALIDATION_ERROR
      ctx.body = ResponseMessages.VALIDATION_ERROR
    }
  }

  public setUserByEmail = async (
    ctx: ContextWithState<UserDataState>,
    next: Next
  ) => {
    const { email } = ctx.state.userData
    ctx.state.user = await User.find()
      .byEmail(email)
      .exec()
    await next()
  }

  public getOrCreateUser = async (
    ctx: ContextWithState<UserDataState<MaybeUserState>>,
    next: Next
  ) => {
    const user = ctx.state.user
    if (user) {
      // User already exists. Nothing else to do
      await next()
    } else {
      // User does not exist. Create it
      await this.create(ctx, next)
    }
  }
}

export default new UserController()
