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
import { SurveyInterface, ItemInterface } from '../clients/pairwise'
import { isObjectId } from './utils'
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
    allowAnon: { type: Boolean, required: true }
  },
  { timestamps: true }
)

const surveySchemaValidator = yup.object().shape({
  apiId: yup.string().required(),
  apiUrl: yup
    .string()
    // .url()
    .required(),
  password: yup
    .string()
    .min(6)
    .max(50)
    .notRequired(),
  allowAnon: yup.bool().required(),
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

/**
 * Survey instance methods
 */
const surveyMethods = {
  passwordMatches(this: ISurvey, password: string) {
    return !this.password
      ? Promise.resolve(false)
      : bcrypt.compare(password, this.password)
  },
  createAnnotator(this: ISurvey, user: IUser) {
    return Annotator.createAnnotator(this, user)
  },
  createAnonAnnotator(this: ISurvey, userName: string, userUuid: string) {
    if (!this.allowAnon) {
      // TODO: Move error message somewhere else
      throw new Error('This survey does not allow anon annotators')
    }
    return Annotator.createAnonAnnotator(this, userName, userUuid)
  },
  async removeAnnotator(
    this: ISurvey,
    annotatorRef: IAnnotator | Types.ObjectId
  ) {
    let annotator = annotatorRef
    if (isObjectId(annotator)) {
      const maybeAnnotator = await Annotator.findById(annotator)
      if (!maybeAnnotator) {
        throw new Error('Annotator not found')
      }
      annotator = maybeAnnotator
    }
    return await annotator.remove()
  },
  getInterface(this: ISurvey) {
    return SurveyInterface.createInterface(this.apiId)
  },
  createItem(this: ISurvey, name: string) {
    return ItemInterface.create(this.apiId, { name })
  },
  getAnnotators(this: ISurvey) {
    return Annotator.find()
      .fromSurvey(this)
      .exec()
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
    name: string,
    allowAnon: boolean,
    password?: string
  ) {
    const survey = await SurveyInterface.create({ name })
    const raw = { apiId: survey.id, apiUrl: survey.url, password, allowAnon }
    return surveySchemaValidator.validate(raw).then(data => this.create(data))
  }
}

/**
 * Survey query helpers
 */
const surveyQueryHelpers = {
  byApiId<T>(this: DocumentQuery<T, ISurvey>, apiId: string) {
    return this.where({ apiId })
  },
  containsAnnotator<T>(this: DocumentQuery<T, ISurvey>, annotator: IAnnotator) {
    let id = annotator.survey
    if (!isObjectId(id)) {
      id = id._id as mongoose.Types.ObjectId
    }
    return this.where({ _id: id })
  },
  fromUser<T>(
    this: DocumentQuery<T, ISurvey>,
    user: IUser | Types.ObjectId | string
  ) {
    if (typeof user === 'string') {
      return this.where({ anonUser: user })
    }
    const userId = isObjectId(user) ? user : (user._id as Types.ObjectId)
    return this.where({ user: userId })
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
  createAnonAnnotator: typeof surveyMethods.createAnonAnnotator
  getInterface: typeof surveyMethods.getInterface
  createItem: typeof surveyMethods.createItem
  getAnnotators: typeof surveyMethods.getAnnotators
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
SurveySchema.query = surveyQueryHelpers

export const Survey = mongoose.model<ISurvey, ISurveyModel>(
  'Survey',
  SurveySchema
)
