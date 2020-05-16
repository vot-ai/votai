import { Next } from 'koa'
import {
  ContextWithState,
  SurveyState,
  SurveyAccessCookieState,
  AuthenticatedUserState
} from '../types/context'
import { UnauthorizedError } from '../errors'
import { ErrorMessages } from '../types/responses'

export const hasSurveyAccess = () => async (
  ctx: ContextWithState<
    SurveyState<SurveyAccessCookieState<AuthenticatedUserState>>
  >,
  next: Next
) => {
  const user = ctx.state.user
  const survey = ctx.state.survey
  // Is it the owner?
  const isOwner = user.isRegistered
    ? survey.user === user._id
    : survey.anonUser === user.uuid
  if (isOwner) {
    return await next()
  }
  // Is it public?
  if (typeof survey.password === 'undefined') {
    // Can non registered or is the user registered?
    if (survey.allowAnon || user.isRegistered) {
      return await next()
    }
  }
  // Does the user have access?
  const hasAccess =
    !!ctx.state.cookies.surveyAccess &&
    ctx.state.cookies.surveyAccess.includes(survey.apiId)
  if (hasAccess) {
    return await next()
  }
  throw new UnauthorizedError(
    ErrorMessages.ACCESS_DENIED,
    `You don't have permission to access the survey ${survey.apiId}`
  )
}
