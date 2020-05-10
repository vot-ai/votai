import * as yup from 'yup'
import { Survey } from '../models/survey'
import { ContextWithState, AuthenticatedUserState } from '../types/context'
import { ResponseStatus, ErrorMessages } from '../types/responses'
import { ValidationError, NotFoundError } from '../errors'

const newSurveyValidator = yup.object().shape({
  name: yup.string().required(),
  allowAnon: yup.boolean().notRequired(),
  password: yup
    .string()
    .min(6)
    .max(50)
    .notRequired(),
  trustAnnotators: yup.boolean().notRequired(),
  maxTime: yup
    .number()
    .min(0)
    .max(60 * 24)
    .integer()
    .notRequired(),
  minViews: yup
    .number()
    .min(0)
    .integer()
    .notRequired(),
  allowConcurrent: yup.boolean().notRequired(),
  base_gamma: yup.number().notRequired(),
  epsilon: yup.number().notRequired()
})

const updateSurveyValidator = newSurveyValidator.clone().shape({
  id: yup.string().required(),
  name: yup.string().notRequired()
})

class SurveyController {
  public async create(ctx: ContextWithState<AuthenticatedUserState>) {
    const user = ctx.state.user
    const raw = ctx.request.body
    let data
    try {
      data = await newSurveyValidator.validate(raw)
    } catch (e) {
      throw new ValidationError(ErrorMessages.COULD_NOT_CREATE_SURVEY, e.errors)
    }
    const survey = await Survey.createSurvey(
      user,
      data,
      data.allowAnon,
      data.password
    )
    ctx.body = await survey.serialize()
    ctx.status = ResponseStatus.OK
  }

  public async update(ctx: ContextWithState<AuthenticatedUserState>) {
    const user = ctx.state.user
    const raw = ctx.request.body
    let data
    try {
      data = await updateSurveyValidator.validate(raw)
    } catch (e) {
      throw new ValidationError(ErrorMessages.COULD_NOT_UPDATE_SURVEY, e.errors)
    }
    const survey = await Survey.findOne()
      .fromUser(user)
      .byApiId(data.id)
    if (!survey) {
      throw new NotFoundError(
        ErrorMessages.SURVEY_NOT_FOUND,
        'Survey does not exist or you do not have write access to it'
      )
    }
    const updatedSurvey = await survey.updateSurvey(data, data.allowAnon)
    ctx.body = await updatedSurvey.serialize()
    ctx.status = ResponseStatus.OK
  }
}

export default new SurveyController()
