/* eslint-disable no-template-curly-in-string */
import mongoose, {
  Document,
  Types,
  Schema,
  DocumentQuery,
  Model
} from 'mongoose'
import * as yup from 'yup'
import bcrypt from 'bcryptjs'
import {
  SurveyInterface,
  ItemInterface,
  NewSurvey,
  NewItem,
  NewAnnotator,
  EditableSurvey
} from '../clients/pairwise'
import { RequestAuthenticatedUser } from '../types/requests'
import { ErrorMessages } from '../types/responses'
import { ValidationError } from '../errors'
import { isObjectId, objectIdSchema } from './utils'
import { IAnnotator, Annotator } from './annotator'
import { IUser } from './user'

/********************************************************************************
 ** Survey
 ********************************************************************************/

/**
 * Actual survey schema with basic information about it
 */
const SurveySchema: Schema = new Schema(
  {
    // Information linking this document to the pairwise API
    apiId: { type: String, required: true, unique: true },
    apiUrl: { type: String, required: true },
    // Security attributes
    password: { type: String, required: false },
    allowAnon: { type: Boolean, required: false, default: false },
    // Owner info
    // Optional related user. If missing, the voter is "anonymous"
    user: {
      type: Schema.Types.ObjectId,
      required: false,
      ref: 'User',
      sparse: true
    },
    // Optional uuid from the anon user
    anonUser: { type: String, required: false, sparse: true }
  },
  { timestamps: true }
)

const passwordValidator = yup
  .string()
  .min(6)
  .max(50)

const surveySchemaValidator = yup.object().shape({
  apiId: yup.string().required(),
  apiUrl: yup
    .string()
    // .url()
    .required(),
  password: passwordValidator.notRequired(),
  allowAnon: yup.bool().required(),
  user: objectIdSchema<IUser>().notRequired(),
  anonUser: yup.string().notRequired(),
  // Meta fields
  createdAt: yup
    .date()
    .default(() => new Date())
    .strip(true),
  updatedAt: yup
    .date()
    .default(() => new Date())
    .strip(true)
})

// Automatically hash passwords before saving to database
SurveySchema.pre<ISurvey>('save', async function(this, next) {
  if (this.isModified('password') && this.password) {
    this.password = await bcrypt.hash(this.password, 10)
  }
  next()
})
// Delete from the API if deleting locally
SurveySchema.post<ISurvey>('remove', async function(doc, next) {
  const survey = await SurveyInterface.createInterface(doc.apiId)
  await survey.delete()
  next()
})
// Remove all related annotators
SurveySchema.post<ISurvey>('remove', async function(doc, next) {
  await Annotator.deleteMany({ survey: doc._id }).exec()
  next()
})

function createAnnotator(
  this: ISurvey,
  user: RequestAuthenticatedUser,
  annotatorData: NewAnnotator
) {
  return Annotator.createAnnotator(this, user, annotatorData)
}

/**
 * Survey instance methods
 */
const surveyMethods = {
  createAnnotator,
  passwordMatches(this: ISurvey, password: string) {
    return !this.password
      ? Promise.resolve(false)
      : bcrypt.compare(password, this.password)
  },
  async changePassword(
    this: ISurvey,
    oldPassword: string,
    newPassword: string
  ) {
    const matches = await this.passwordMatches(oldPassword)
    if (!matches) {
      throw new ValidationError(
        ErrorMessages.INVALID_PASSWORD,
        'Could not change password. Old password is invalid'
      )
    }
    const password = await passwordValidator.validate(newPassword)
    this.password = password
    return await this.save()
  },
  async removeAnnotator(
    this: ISurvey,
    annotatorRef: IAnnotator | Types.ObjectId
  ) {
    let annotator = annotatorRef
    if (isObjectId(annotator)) {
      const maybeAnnotator = await Annotator.findById(annotator)
      if (!maybeAnnotator) {
        throw new ValidationError(
          ErrorMessages.ANNOTATOR_NOT_FOUND,
          'Annotator does not exist'
        )
      }
      annotator = maybeAnnotator
    }
    return await annotator.remove()
  },
  getInterface(this: ISurvey) {
    return SurveyInterface.createInterface(this.apiId)
  },
  createItem(this: ISurvey, itemData: NewItem) {
    return ItemInterface.create(this.apiId, itemData)
  },
  getAnnotators(this: ISurvey) {
    return Annotator.find()
      .fromSurvey(this)
      .exec()
  },
  async serialize(this: ISurvey) {
    const api = await this.getInterface()
    const data = {
      // API data
      id: api.id,
      name: api.name,
      active: api.active,
      max_time: api.max_time,
      min_views: api.min_views,
      allowConcurrent: api.allow_concurrent,
      trustAnnotators: api.trust_annotators,
      epsilon: api.epsilon,
      gamma: api.gamma,
      base_gamma: api.base_gamma,
      tau: api.tau,
      dynamic_gamma: api.dynamic_gamma,
      // Local data
      allowAnon: this.allowAnon,
      private: !!this.password
    }
    return data
  },
  async updateSurvey(
    this: ISurvey,
    surveyData?: EditableSurvey,
    allowAnon?: boolean
  ) {
    if (surveyData) {
      const apiInterface = await this.getInterface()
      await apiInterface.patch(surveyData)
    }
    if (typeof allowAnon !== 'undefined') {
      this.allowAnon = allowAnon
      await this.save()
    }
    return this
  }
}

/**
 * Survey model methods
 */
const surveyStatics = {
  findByApiId(this: ISurveyModel, apiId: string) {
    return this.findOne().byApiId(apiId)
  },
  findByAnnotator(this: ISurveyModel, annotator: IAnnotator) {
    return this.findOne().containsAnnotator(annotator)
  },
  async createSurvey(
    this: ISurveyModel,
    user: RequestAuthenticatedUser,
    surveyData: NewSurvey,
    allowAnon?: boolean,
    password?: string
  ) {
    const survey = await SurveyInterface.create(surveyData)
    const data: Partial<ISurvey> = {
      apiId: survey.id,
      apiUrl: survey.url,
      password,
      allowAnon
    }
    if (user.isRegistered) {
      data.user = user._id
    } else {
      data.anonUser = user.uuid
    }
    return this.create(data)
  }
}

/**
 * Survey query helpers
 */
const surveyQueryHelpers = {
  byApiId<T extends DocumentQuery<any, ISurvey>>(this: T, apiId: string) {
    return this.where({ apiId })
  },
  containsAnnotator<T extends DocumentQuery<any, ISurvey>>(
    this: T,
    annotator: IAnnotator
  ) {
    let id = annotator.survey
    if (!isObjectId(id)) {
      id = id._id as mongoose.Types.ObjectId
    }
    return this.where({ _id: id })
  },
  fromUser<T extends DocumentQuery<any, ISurvey>>(
    this: T,
    user: RequestAuthenticatedUser
  ) {
    if (!user.isRegistered) {
      return this.where({ anonUser: user.uuid })
    }
    return this.where({ user: user._id })
  }
}

/**
 * Type of the Survey Instance
 */
export interface ISurvey
  extends Document,
    yup.InferType<typeof surveySchemaValidator> {
  passwordMatches: typeof surveyMethods.passwordMatches
  createAnnotator: typeof surveyMethods.createAnnotator
  getInterface: typeof surveyMethods.getInterface
  createItem: typeof surveyMethods.createItem
  getAnnotators: typeof surveyMethods.getAnnotators
  serialize: typeof surveyMethods.serialize
  changePassword: typeof surveyMethods.changePassword
  updateSurvey: typeof surveyMethods.updateSurvey
}
/**
 * Type of the Survey Model
 */
export interface ISurveyModel
  extends Model<ISurvey, typeof surveyQueryHelpers> {
  findByApiId: typeof surveyStatics.findByApiId
  findByAnnotator: typeof surveyStatics.findByAnnotator
  createSurvey: typeof surveyStatics.createSurvey
}

// Register interface and model methods
SurveySchema.statics = surveyStatics
SurveySchema.methods = surveyMethods
// SurveySchema.query = surveyQueryHelpers
SurveySchema.query.byApiId = surveyQueryHelpers.byApiId
SurveySchema.query.fromUser = surveyQueryHelpers.fromUser

export const Survey = mongoose.model<ISurvey, ISurveyModel>(
  'Survey',
  SurveySchema
)
