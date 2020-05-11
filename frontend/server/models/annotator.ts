/* eslint-disable no-template-curly-in-string */
import mongoose, {
  Document,
  Types,
  Schema,
  DocumentQuery,
  Model
} from 'mongoose'
import * as yup from 'yup'
import consola from 'consola'
import { RequestAuthenticatedUser } from '../types/requests'
import { NewAnnotator, AnnotatorInterface } from '../clients/pairwise'
import { ErrorMessages } from '../types/responses'
import { ServerError } from '../errors'
import { IUser } from './user'
import { ISurvey, Survey } from './survey'
import { isObjectId, objectIdSchema } from './utils'
/********************************************************************************
 ** Annotator
 ********************************************************************************/

/**
 * Annotator that may be anonymous
 */
const AnnotatorSchema: Schema = new Schema({
  // Information linking this document to the pairwise API
  apiId: { type: String, required: true, unique: true },
  apiUrl: { type: String, required: true },
  // Optional related user. If missing, the voter is "anonymous"
  user: {
    type: Schema.Types.ObjectId,
    required: false,
    ref: 'User',
    sparse: true
  },
  // Optional uuid from the anon user
  anonUser: { type: String, required: false, sparse: true },
  // Survey reference
  survey: {
    type: Schema.Types.ObjectId,
    required: true,
    ref: 'Survey',
    index: true
  }
})

// From regular JS to a document
const annotatorSchemaValidator = yup.object().shape({
  apiId: yup.string().required(),
  apiUrl: yup.string().required(),
  user: objectIdSchema<IUser>().notRequired(),
  anonUser: yup.string().notRequired(),
  survey: objectIdSchema<ISurvey>().required()
})

const autoPopulateSurvey: mongoose.HookSyncCallback<IAnnotator> = function(
  next
) {
  this.populate('survey')
  next()
}

// Always populate on load
AnnotatorSchema.pre('find', autoPopulateSurvey)
AnnotatorSchema.pre('findOne', autoPopulateSurvey)

// Delete from the API if deleting locally
AnnotatorSchema.post<IAnnotator>('remove', async function(
  doc: IAnnotator,
  next
) {
  let survey = doc.survey
  if (isObjectId(survey)) {
    const maybeSurvey = await Survey.findOne({ _id: doc.survey })
      .select('apiId')
      .exec()
    if (!maybeSurvey) {
      return next(
        new ServerError(
          ErrorMessages.SURVEY_NOT_FOUND,
          `Could not find related Survey when deleting annotator ${doc.apiId}`
        )
      )
    }
    survey = maybeSurvey
  }
  let annotator
  try {
    annotator = await AnnotatorInterface.createInterface(
      survey.apiId,
      doc.apiId
    )
  } catch (e) {
    // Log but do not handle the error
    consola.error(e)
    return next()
  }
  await annotator.delete()
  next()
})

/**
 * Annotator instance methods
 */
const annotatorMethods = {
  async getInterface(this: IAnnotator) {
    let survey = this.survey
    if (isObjectId(survey)) {
      const maybeSurvey = await Survey.findById(survey).exec()
      if (!maybeSurvey) {
        throw new ServerError(
          ErrorMessages.SURVEY_NOT_FOUND,
          'Survey does not exist on the API'
        )
      }
      survey = maybeSurvey
    }
    return await AnnotatorInterface.createInterface(survey.apiId, this.apiId)
  }
}

async function createAnnotator(
  this: IAnnotatorModel,
  survey: ISurvey,
  user: RequestAuthenticatedUser,
  annotatorData: NewAnnotator
) {
  let annotator
  let raw
  if (user.isRegistered) {
    const data = { ...annotatorData, name: user.name }
    annotator = await AnnotatorInterface.create(survey.apiId, data)
    raw = { user: user._id }
  } else {
    annotator = await AnnotatorInterface.create(survey.apiId, annotatorData)
    raw = { anonUser: user.uuid }
  }
  raw = {
    ...raw,
    apiId: annotator.id,
    apiUrl: annotator.url,
    survey: survey._id
  }
  return await annotatorSchemaValidator
    .validate(raw)
    .then(data => this.create(data))
}

/**
 * Annotator model methods
 */
const annotatorStatics = {
  createAnnotator
}

/**
 * Annotator query helpers
 */
const annotatorQueryHelpers = {
  byApiId<T extends DocumentQuery<any, IAnnotator>>(this: T, apiId: string) {
    return this.where({ apiId })
  },
  fromUser<T extends DocumentQuery<any, IAnnotator>>(
    this: T,
    user: RequestAuthenticatedUser
  ) {
    if (!user.isRegistered) {
      return this.where({ anonUser: user.uuid })
    }
    return this.where({ user: user._id })
  },
  fromSurvey<T extends DocumentQuery<any, IAnnotator>>(
    this: T,
    survey: ISurvey | Types.ObjectId
  ) {
    const surveyId = isObjectId(survey)
      ? survey
      : (survey._id as Types.ObjectId)
    return this.where({ survey: surveyId })
  }
}

// Register interface and model methods
AnnotatorSchema.statics = annotatorStatics
AnnotatorSchema.methods = annotatorMethods
AnnotatorSchema.query = annotatorQueryHelpers

/**
 * Type of the Annotator Instance
 */
export interface IAnnotator
  extends Document,
    yup.InferType<typeof annotatorSchemaValidator> {
  getInterface: typeof annotatorMethods.getInterface
}
/**
 * Type of the Annotator Model
 */
export interface IAnnotatorModel
  extends Model<IAnnotator, typeof annotatorQueryHelpers> {
  createAnnotator: typeof annotatorStatics.createAnnotator
}

export const Annotator = mongoose.model<IAnnotator, IAnnotatorModel>(
  'Annotator',
  AnnotatorSchema
)
