import { ISurvey } from '~/server/models/survey'
import { IAnnotator } from '~/server/models/annotator'
import { ThenArg } from '~/types/utils'
export type SerializedSurvey = ThenArg<ReturnType<ISurvey['serialize']>>
export type SerializedAnnotator = ThenArg<
  ReturnType<IAnnotator['serializeForVote']>
>
export type SerializedItem = ThenArg<ReturnType<IAnnotator['serializeItem']>>
