import { Next } from 'koa'
import {
  ContextWithState,
  SurveyState,
  AuthenticatedUserState
} from '../types/context'
import { Annotator } from '../models/annotator'
import { UnauthorizedError } from '../errors'
import { ErrorMessages } from '../types/responses'

export const userIsAnnotator = () => async (
  ctx: ContextWithState<SurveyState<AuthenticatedUserState>>,
  next: Next
) => {
  const user = ctx.state.user
  const survey = ctx.state.survey
  const annotator = await Annotator.findOne()
    .fromUser(user)
    .fromSurvey(survey)
    .exec()
  if (!annotator) {
    throw new UnauthorizedError(
      ErrorMessages.ANNOTATOR_NOT_FOUND,
      `You are not an annotator of the survey ${survey.apiId}`
    )
  }
  ctx.state.annotator = annotator
  await next()
}
