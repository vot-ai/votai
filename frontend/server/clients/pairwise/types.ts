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

// TODO: Revert this. Vue cant handle recursion
// type MetadataKey = string | number | Metadata
type MetadataKey = any

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
  trust_annotators?: boolean
  base_gamma?: number
  epsilon?: number
  tau?: number
  dynamic_gamma?: boolean
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
  max_budget: number
  min_budget: number
  budget: number
  consumed_budget: number
  gamma: number
}

/********************************************************************************
 ** Annotator
 ********************************************************************************/

export type AnnotatorId = string

export type NewAnnotator = {
  name: string
  metadata?: Metadata
  active?: boolean
  alpha?: number
  beta?: number
}

export type EditableAnnotator = Partial<NewAnnotator>

export type Annotator = Required<NewAnnotator> & {
  url: string
  id: string
  survey: string
  current: string | null
  previous: string | null
  vote: string
  skip: string
  quality: number
  items_left: number
}

export type AnnotatorActionResponse = {
  current: Item | null
  previous: Item | null
  vote: string
  skip: string
  items_left: number
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
