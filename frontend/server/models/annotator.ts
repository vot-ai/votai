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
import { AnnotatorInterface } from '../clients/pairwise'
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
        Error(
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
    consola.log(
      'The following error was probably caused because the annotator does not exist anymore'
    )
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
        // TODO: Think of a better error message and move it somewhere else
        throw new Error('Survey not found')
      }
      survey = maybeSurvey
    }
    return await AnnotatorInterface.createInterface(survey.apiId, this.apiId)
  }
}

/**
 * Annotator model methods
 */
const annotatorStatics = {
  async createAnnotator(this: IAnnotatorModel, survey: ISurvey, user: IUser) {
    const annotator = await AnnotatorInterface.create(survey.apiId, {
      name: user.name
    })
    const raw = {
      apiId: annotator.id,
      apiUrl: annotator.url,
      survey: survey._id,
      user: user._id
    }
    return await annotatorSchemaValidator
      .validate(raw)
      .then(data => this.create(data))
  },
  async createAnonAnnotator(
    this: IAnnotatorModel,
    survey: ISurvey,
    userName: string,
    userUuid: string
  ) {
    const annotator = await AnnotatorInterface.create(survey.apiId, {
      name: userName
    })
    const raw = {
      apiId: annotator.id,
      apiUrl: annotator.url,
      survey: survey._id,
      anonUser: userUuid
    }
    return await annotatorSchemaValidator
      .validate(raw)
      .then(data => this.create(data))
  }
}

/**
 * Annotator query helpers
 */
const annotatorQueryHelpers = {
  byApiId<T>(this: DocumentQuery<T, IAnnotator>, apiId: string) {
    return this.where({ apiId })
  },
  fromUser<T>(
    this: DocumentQuery<T, IAnnotator>,
    user: IUser | Types.ObjectId | string
  ) {
    if (typeof user === 'string') {
      return this.where({ anonUser: user })
    }
    const userId = isObjectId(user) ? user : (user._id as Types.ObjectId)
    return this.where({ user: userId })
  },
  fromSurvey<T>(
    this: DocumentQuery<T, IAnnotator>,
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
  createAnonAnnotator: typeof annotatorStatics.createAnonAnnotator
}

export const Annotator = mongoose.model<IAnnotator, IAnnotatorModel>(
  'Annotator',
  AnnotatorSchema
)
