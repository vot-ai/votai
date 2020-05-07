/* eslint-disable camelcase */

export interface ListResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

/********************************************************************************
 ** Survey
 ********************************************************************************/

export type SurveyId = string

type MetadataKey = string | number | Metadata

export type Metadata = {
  [key: string]: MetadataKey | MetadataKey[]
}

export type NewSurvey = {
  name: string
  metadata?: Metadata
  active?: boolean
  max_time?: number
  min_views?: number
  allow_concurrent?: boolean
  gamma?: number
  epsilon?: number
}

export type EditableSurvey = Partial<NewSurvey>

export type Survey = Required<NewSurvey> & {
  url: string
  id: string
  items: string[]
  ranking: string[]
  annotators: string[]
  created: string
  updated: string
  max_annotators: number
  max_items: number
}

/********************************************************************************
 ** Annotator
 ********************************************************************************/

export type AnnotatorId = string

export type NewAnnotator = {
  name: string
  metadata?: Metadata
  active?: boolean
}

export type EditableAnnotator = Partial<NewAnnotator>

export type Annotator = Required<NewAnnotator> & {
  url: string
  id: string
  survey: string
  current: string
  previous: string
  vote: string
  skip: string
  alpha: number
  beta: number
  quality: number
}

export type AnnotatorActionResponse = {
  current: Item | null
  previous: Item | null
  vote: string
  skip: string
}

/********************************************************************************
 ** Item
 ********************************************************************************/

export type ItemId = string

export type NewItem = {
  name: string
  metadata?: Metadata
}

export type EditableItem = Partial<NewItem>

export type Item = Required<NewItem> & {
  url: string
  id: string
  survey: string
  prioritize: string
  deprioritize: string
  active: boolean
  prioritized: boolean
  mu: number
  sigma_squared: number
}
