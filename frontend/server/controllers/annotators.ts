import * as yup from 'yup'
import {
  ContextWithState,
  AuthenticatedUserState,
  SurveyState,
  AnnotatorState
} from '../types/context'
import { ResponseStatus, ErrorMessages } from '../types/responses'
import { ValidationError } from '../errors'
import { NewAnnotator } from '../clients/pairwise'
import { Annotator } from '../models/annotator'

const voteValidator = yup.object().shape({
  currentWins: yup.boolean().required()
})

class AnnotatorController {
  public async getAnnotator(
    ctx: ContextWithState<SurveyState<AuthenticatedUserState>>
  ) {
    const user = ctx.state.user
    const survey = ctx.state.survey
    // Check if the user is already an annotator
    let annotator = await Annotator.findOne()
      .fromUser(user)
      .fromSurvey(survey)
      .exec()
    if (!annotator) {
      // If the annotator does not exist, create it
      let annotatorData: NewAnnotator
      if (user.isRegistered) {
        annotatorData = { name: user.name, active: true }
      } else {
        annotatorData = {
          name: `Anon ${user.uuid.split('-')[0]}`,
          active: true
        }
      }
      annotator = await survey.createAnnotator(user, annotatorData)
    }
    await annotator.updateChoices()
    ctx.body = await annotator.serializeForVote()
    ctx.status = ResponseStatus.OK
  }

  public async updateChoices(ctx: ContextWithState<AnnotatorState>) {
    const annotator = ctx.state.annotator
    await annotator.updateChoices()
    ctx.body = await annotator.serializeForVote()
    ctx.status = ResponseStatus.OK
  }

  public async vote(ctx: ContextWithState<SurveyState<AnnotatorState>>) {
    const annotator = ctx.state.annotator
    const raw = ctx.request.body
    let data
    try {
      data = await voteValidator.validate(raw)
    } catch (e) {
      throw new ValidationError(ErrorMessages.COULD_NOT_VOTE, e.errors)
    }
    await annotator.vote(data.currentWins)
    ctx.body = await annotator.serializeForVote()
    ctx.status = ResponseStatus.OK
  }

  public async skip(ctx: ContextWithState<SurveyState<AnnotatorState>>) {
    const annotator = ctx.state.annotator
    await annotator.skip()
    ctx.body = await annotator.serializeForVote()
    ctx.status = ResponseStatus.OK
  }
}

export default new AnnotatorController()
