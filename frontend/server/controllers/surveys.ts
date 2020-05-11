import Koa from 'koa'
import { ParamMiddleware } from '@koa/router'
import * as yup from 'yup'
import { Survey } from '../models/survey'
import {
  ContextWithState,
  AuthenticatedUserState,
  UnknownUserState,
  SurveyState,
  SurveyAccessCookieState
} from '../types/context'
import {
  ResponseStatus,
  ErrorMessages,
  ResponseMessages
} from '../types/responses'
import { ValidationError, NotFoundError, ForbiddenError } from '../errors'

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
  name: yup.string().notRequired()
})

const requestAccessValidator = yup.object().shape({
  password: yup
    .string()
    .min(6)
    .max(50)
    .required()
})

const changePasswordValidator = requestAccessValidator.clone().shape({
  oldPassword: yup
    .string()
    .min(6)
    .max(50)
    .required()
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

  public async update(
    ctx: ContextWithState<AuthenticatedUserState<SurveyState>>
  ) {
    const user = ctx.state.user
    const survey = ctx.state.survey
    const isOwner = user.isRegistered
      ? user._id === survey.user
      : user.uuid === survey.anonUser
    if (!isOwner) {
      throw new ForbiddenError(
        ErrorMessages.ACCESS_DENIED,
        'You do not have write access to this survey'
      )
    }
    let data
    try {
      data = await updateSurveyValidator.validate(ctx.request.body)
    } catch (e) {
      throw new ValidationError(ErrorMessages.COULD_NOT_UPDATE_SURVEY, e.errors)
    }

    const updatedSurvey = await survey.updateSurvey(data, data.allowAnon)
    ctx.body = await updatedSurvey.serialize()
    ctx.status = ResponseStatus.OK
  }

  public async delete(
    ctx: ContextWithState<AuthenticatedUserState<SurveyState>>
  ) {
    const user = ctx.state.user
    const survey = ctx.state.survey
    const isOwner = user.isRegistered
      ? user._id === survey.user
      : user.uuid === survey.anonUser
    if (!isOwner) {
      throw new ForbiddenError(
        ErrorMessages.ACCESS_DENIED,
        'You do not have write access to this survey'
      )
    }
    await survey.remove()
    ctx.body = ResponseMessages.DELETED
    ctx.status = ResponseStatus.DELETED
  }

  public async changePassword(
    ctx: ContextWithState<AuthenticatedUserState<SurveyState>>
  ) {
    const user = ctx.state.user
    const survey = ctx.state.survey
    const isOwner = user.isRegistered
      ? user._id === survey.user
      : user.uuid === survey.anonUser
    if (!isOwner) {
      throw new ForbiddenError(
        ErrorMessages.ACCESS_DENIED,
        'You do not have write access to this survey'
      )
    }
    let data
    try {
      data = await changePasswordValidator.validate(ctx.request.body)
    } catch (e) {
      throw new ValidationError(ErrorMessages.INVALID_PASSWORD, e.errors)
    }

    const updatedSurvey = await survey.changePassword(
      data.oldPassword,
      data.password
    )
    ctx.body = await updatedSurvey.serialize()
    ctx.status = ResponseStatus.OK
  }

  public surveyParam: ParamMiddleware = async (
    surveyId,
    ctx: Koa.ParameterizedContext<UnknownUserState>,
    next
  ) => {
    const survey = await Survey.findByApiId(surveyId)
    if (!survey) {
      throw new NotFoundError(
        ErrorMessages.SURVEY_NOT_FOUND,
        `Survey ${surveyId} does not exist or you do not have access to it`
      )
    }
    ctx.state.survey = survey
    await next()
  }

  public async get(
    ctx: ContextWithState<
      SurveyState<UnknownUserState<SurveyAccessCookieState>>
    >
  ) {
    const user = ctx.state.user
    const survey = ctx.state.survey
    const hasAccess =
      !!ctx.state.cookies.surveyAccess &&
      ctx.state.cookies.surveyAccess.includes(survey.apiId)
    // Check if is the owner
    if (user.isAuthenticated) {
      const isOwner = user.isRegistered
        ? survey.user === user._id
        : survey.anonUser === user.uuid
      if (isOwner) {
        ctx.body = await survey.serialize()
        ctx.status = ResponseStatus.OK
        return
      }
    }
    // Or has access
    if (hasAccess) {
      ctx.body = await survey.serialize()
      ctx.status = ResponseStatus.OK
      return
    }
    // Else, return basic serialized data
    ctx.body = await survey.reducedSerialize()
    ctx.status = ResponseStatus.OK
  }

  public async listUserOwned(ctx: ContextWithState<AuthenticatedUserState>) {
    const user = ctx.state.user
    const userSurveys = await Survey.find()
      .fromUser(user)
      .sort('createdAt')
      .exec()
    ctx.body = await Promise.all(userSurveys.map(survey => survey.serialize()))
    ctx.status = ResponseStatus.OK
  }

  public async listFromAnnotator(
    ctx: ContextWithState<AuthenticatedUserState>
  ) {
    const user = ctx.state.user
    const userSurveys = await Survey.find().containsAnnotator(user)
    const serializedSurveys = await Promise.all(
      userSurveys.map(survey => survey.serialize())
    )
    ctx.status = ResponseStatus.OK
    ctx.body = serializedSurveys
  }

  public async requestAccess(
    ctx: ContextWithState<SurveyState<SurveyAccessCookieState>>
  ) {
    const raw = ctx.request.body
    let data
    try {
      data = await requestAccessValidator.validate(raw)
    } catch (err) {
      throw new ValidationError(ResponseMessages.VALIDATION_ERROR, err.errors)
    }
    const survey = ctx.state.survey
    const matches = await survey.passwordMatches(data.password)
    if (matches) {
      if (ctx.state.cookies.surveyAccess) {
        ctx.state.cookies.surveyAccess.push(survey.apiId)
      } else {
        ctx.state.cookies.surveyAccess = [survey.apiId]
      }
      ctx.state.cookies.surveyAccess = Array.from(
        new Set(ctx.state.cookies.surveyAccess)
      )
      ctx.status = ResponseStatus.OK
      ctx.body = ResponseMessages.OK
    } else {
      // Wait a while before responding
      await new Promise(resolve =>
        setTimeout(() => {
          resolve()
        }, 5000)
      )
      throw new ValidationError(
        ErrorMessages.INVALID_PASSWORD,
        `Invalid password for survey ${survey.apiId}`
      )
    }
  }
}

export default new SurveyController()
