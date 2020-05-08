import { Next } from 'koa'
import { ContextWithState, UnknownUserState } from '../types/context'
import { ResponseStatus, ResponseMessages } from '../types/responses'
import { isRegistered, isAuthenticated } from './auth'

/**
 * User must be registered
 */
export const loginRequired = () => async (
  ctx: ContextWithState<UnknownUserState>,
  next: Next
) => {
  const unkownUser = ctx.state.user
  if (isRegistered(unkownUser)) {
    await next()
  } else {
    ctx.status = ResponseStatus.UNAUTHORIZED_ERROR
    ctx.body = ResponseMessages.UNAUTHORIZED_ERROR
  }
}

/**
 * User may be registered or anonymous (with a token)
 */
export const authenticationRequired = () => async (
  ctx: ContextWithState<UnknownUserState>,
  next: Next
) => {
  const unkownUser = ctx.state.user
  if (isAuthenticated(unkownUser)) {
    await next()
  } else {
    ctx.status = ResponseStatus.UNAUTHORIZED_ERROR
    ctx.body = ResponseMessages.UNAUTHORIZED_ERROR
  }
}

/**
 * Allows any user
 */
export const allowAny = () => (
  _ctx: ContextWithState<UnknownUserState>,
  next: Next
) => {
  next()
}
