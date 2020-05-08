/* eslint-disable no-template-curly-in-string */
import mongoose, { Types } from 'mongoose'
import * as yup from 'yup'

export const isObjectId = (value: any): value is Types.ObjectId =>
  mongoose.Types.ObjectId.isValid(value)
export const isUndefOrObjectId = (
  value: any
): value is Types.ObjectId | undefined =>
  typeof value === 'undefined' || mongoose.Types.ObjectId.isValid(value)
export const objectIdSchema = <T>() =>
  (yup
    .object()
    .test(
      'is-object-id',
      '${path} is not a valid object ID',
      isUndefOrObjectId
    ) as unknown) as yup.MixedSchema<Types.ObjectId | T>
