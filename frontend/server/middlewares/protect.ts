import { Next } from 'koa'
import { ContextWithState, UnknownUserState } from '../types/context'
import { UnauthorizedError } from '../errors'
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
    throw new UnauthorizedError()
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
    throw new UnauthorizedError()
  }
}

/**
 * Allows any user
 */
export const allowAny = () => async (
  _ctx: ContextWithState<UnknownUserState>,
  next: Next
) => {
  await next()
}
