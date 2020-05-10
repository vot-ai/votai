import Axios, { AxiosRequestConfig, AxiosResponse } from 'axios'
import {
  NewSurvey,
  EditableSurvey,
  SurveyId,
  Survey,
  Annotator,
  ListResponse,
  Item,
  AnnotatorId,
  NewAnnotator,
  AnnotatorActionResponse,
  ItemId,
  NewItem,
  EditableItem,
  EditableAnnotator
} from './types'

export const pairwiseAxios = Axios.create({
  baseURL: 'http://backend:8000',
  headers: {
    Authorization: `Token ${process.env.PAIRWISE_API_TOKEN}`,
    Accept: 'application/json'
  }
})

export class PairwiseClient {
  async request<T = any>(config: AxiosRequestConfig) {
    const response = await pairwiseAxios(config)
    return response as AxiosResponse<T>
  }

  async paginatedRequest<T = any>(
    config: AxiosRequestConfig,
    page = 0,
    pageSize = 10
  ) {
    const limit = pageSize
    const offset = page * pageSize
    const params = { ...config.params, limit, offset }
    const method: 'GET' = 'GET'
    const paginatedConfig = { method, ...config, params }
    return await this.request<ListResponse<T>>(paginatedConfig)
  }

  /********************************************************************************
   ** Survey methods
   ********************************************************************************/
  async getSurvey(id: SurveyId) {
    const response = await this.request<Survey>({
      method: 'GET',
      url: `/surveys/${id}/`
    })
    return response.data
  }

  async createSurvey(data: NewSurvey) {
    const response = await this.request<Survey>({
      method: 'POST',
      url: '/surveys/',
      data
    })
    return response.data
  }

  async updateSurvey(id: SurveyId, data: EditableSurvey) {
    const response = await this.request<Survey>({
      method: 'PATCH',
      url: `/surveys/${id}/`,
      data
    })
    return response.data
  }

  async deleteSurvey(id: SurveyId) {
    await this.request({
      method: 'DELETE',
      url: `/surveys/${id}/`
    })
    return true
  }

  async getSurveyAnnotators(
    surveyId: string,
    page?: number,
    pageSize?: number
  ) {
    const response = await this.paginatedRequest<Annotator>(
      {
        url: `/surveys/${surveyId}/annotators/`
      },
      page,
      pageSize
    )
    return response.data
  }

  async getSurveyItems(surveyId: string, page?: number, pageSize?: number) {
    const response = await this.paginatedRequest<Item>(
      {
        url: `/surveys/${surveyId}/items/`
      },
      page,
      pageSize
    )
    return response.data
  }

  async getSurveyRanking(surveyId: string, page?: number, pageSize?: number) {
    const response = await this.paginatedRequest<Item>(
      {
        url: `/surveys/${surveyId}/ranking/`
      },
      page,
      pageSize
    )
    return response.data
  }

  /********************************************************************************
   ** Annotator methods
   ********************************************************************************/
  async getAnnotator(id: AnnotatorId, surveyId: SurveyId) {
    const response = await this.request<Annotator>({
      method: 'GET',
      url: `/surveys/${surveyId}/annotators/${id}/`
    })
    return response.data
  }

  async createAnnotator(data: NewAnnotator, surveyId: SurveyId) {
    const response = await this.request<Annotator>({
      method: 'POST',
      url: `/surveys/${surveyId}/annotators/`,
      data
    })
    return response.data
  }

  async updateAnnotator(
    id: AnnotatorId,
    data: EditableAnnotator,
    surveyId: SurveyId
  ) {
    const response = await this.request<Annotator>({
      method: 'PATCH',
      url: `/surveys/${surveyId}/annotators/${id}/`,
      data
    })
    return response.data
  }

  async deleteAnnotator(id: AnnotatorId, surveyId: SurveyId) {
    await this.request({
      method: 'DELETE',
      url: `/surveys/${surveyId}/annotators/${id}/`
    })
    return true
  }

  async annotatorSkip(id: AnnotatorId, surveyId: SurveyId) {
    const response = await this.request<AnnotatorActionResponse>({
      method: 'POST',
      url: `/surveys/${surveyId}/annotators/${id}/skip/`
    })
    return response.data
  }

  async annotatorVote(
    id: AnnotatorId,
    surveyId: SurveyId,
    currentWins: boolean
  ) {
    const response = await this.request<AnnotatorActionResponse>({
      method: 'POST',
      url: `/surveys/${surveyId}/annotators/${id}/vote/`,
      data: {
        current_wins: currentWins
      }
    })
    return response.data
  }

  /********************************************************************************
   ** Item methods
   ********************************************************************************/
  async getItem(id: ItemId, surveyId: SurveyId) {
    const response = await this.request<Item>({
      method: 'GET',
      url: `/surveys/${surveyId}/items/${id}/`
    })
    return response.data
  }

  async createItem(data: NewItem, surveyId: SurveyId) {
    const response = await this.request<Item>({
      method: 'POST',
      url: `/surveys/${surveyId}/items/`,
      data
    })
    return response.data
  }

  async updateItem(id: ItemId, data: EditableItem, surveyId: SurveyId) {
    const response = await this.request<Item>({
      method: 'PATCH',
      url: `/surveys/${surveyId}/items/${id}/`,
      data
    })
    return response.data
  }

  async deleteItem(id: ItemId, surveyId: SurveyId) {
    await this.request({
      method: 'DELETE',
      url: `/surveys/${surveyId}/items/${id}/`
    })
    return true
  }

  async itemPrioritize(id: ItemId, surveyId: SurveyId) {
    const response = await this.request<Item>({
      method: 'POST',
      url: `/surveys/${surveyId}/items/${id}/prioritize/`
    })
    return response.data
  }

  async itemDeprioritize(id: ItemId, surveyId: SurveyId) {
    const response = await this.request<Item>({
      method: 'POST',
      url: `/surveys/${surveyId}/items/${id}/deprioritize/`
    })
    return response.data
  }
}

abstract class BaseInterface<T> {
  protected readonly surveyId: SurveyId
  protected readonly client: PairwiseClient
  protected self: T = (null as unknown) as T
  protected _survey: SurveyInterface | null = null

  protected constructor(surveyId: SurveyId, self: T) {
    this.surveyId = surveyId
    this.client = new PairwiseClient()
    this.setSelf(self)
  }

  protected abstract async fetchSelf(): Promise<T>
  abstract async delete(): Promise<boolean>
  abstract async patch(
    update: Partial<T>
  ): Promise<ThisType<new (...args: any[]) => BaseInterface<T>>>

  protected get survey() {
    if (this._survey) {
      return Promise.resolve(this._survey)
    } else {
      return this.client
        .getSurvey(this.surveyId)
        .then(survey => new SurveyInterface(survey.id, survey))
    }
  }

  protected setSelf(self: T) {
    this.self = self
    for (const key in self) {
      if (!(key in this)) {
        ;((this as unknown) as T)[key] = self[key]
      }
    }
    return this
  }

  async update() {
    return this.setSelf(await this.fetchSelf())
  }

  static createInterface<T extends BaseInterface<T>>(
    this: new (surveyId: SurveyId, self: T) => BaseInterface<T>,
    _surveyId: SurveyId,
    _self: T
  ): Promise<
    InstanceType<new (surveyId: SurveyId, self: T) => BaseInterface<T> & T>
  > {
    return {} as any
  }
}

export class ItemInterface extends BaseInterface<Item> {
  readonly id: ItemId

  protected constructor(surveyId: SurveyId, self: Item) {
    super(surveyId, self)
    this.id = self.id
  }

  protected async fetchSelf() {
    return await this.client.getItem(this.id, this.surveyId)
  }

  async prioritize() {
    await this.client
      .itemPrioritize(this.id, this.surveyId)
      .then(this.setSelf.bind(this))
    return this
  }

  async deprioritize() {
    await this.client
      .itemDeprioritize(this.id, this.surveyId)
      .then(this.setSelf.bind(this))
    return this
  }

  async delete() {
    return await this.client.deleteItem(this.id, this.surveyId)
  }

  async patch(update: EditableItem) {
    const self = await this.client.updateItem(this.id, update, this.surveyId)
    return this.setSelf(self)
  }

  static async create(surveyId: SurveyId, data: NewItem) {
    const item = await new PairwiseClient().createItem(data, surveyId)
    return this.createInterface(surveyId, item)
  }

  static async createInterface(
    surveyId: SurveyId,
    self: Item
  ): Promise<Readonly<Item> & ItemInterface>
  static async createInterface(
    surveyId: SurveyId,
    id: ItemId
  ): Promise<Readonly<Item> & ItemInterface>
  static async createInterface(surveyId: SurveyId, idOrSelf: ItemId | Item) {
    let item = idOrSelf
    if (typeof item === 'string') {
      item = await new PairwiseClient().getItem(item, surveyId)
    }
    return new ItemInterface(surveyId, item as Item) as ItemInterface & Item
  }
}

export class AnnotatorInterface extends BaseInterface<Annotator> {
  readonly id: AnnotatorId
  private _current: (ItemInterface & Item) | null = null
  private _previous: (ItemInterface & Item) | null = null

  protected constructor(surveyId: SurveyId, self: Annotator) {
    super(surveyId, self)
    this.id = self.id
  }

  protected async fetchSelf() {
    return await this.client.getAnnotator(this.id, this.surveyId)
  }

  get current() {
    if (this._current) {
      return Promise.resolve(this._current)
    }
    return this.client
      .request<Item>({ method: 'GET', url: this.self.current })
      .then(response => response.data)
      .then(current => {
        return ItemInterface.createInterface(this.surveyId, current)
      })
  }

  get previous() {
    if (this._previous) {
      return Promise.resolve(this._previous)
    }
    return this.client
      .request<Item>({ method: 'GET', url: this.self.previous })
      .then(response => response.data)
      .then(previous => {
        return ItemInterface.createInterface(this.surveyId, previous)
      })
  }

  async skip() {
    const response = await this.client.annotatorSkip(this.id, this.surveyId)
    if (response.current) {
      this._current = await ItemInterface.createInterface(
        this.surveyId,
        response.current
      )
    }
    if (response.previous) {
      this._previous = await ItemInterface.createInterface(
        this.surveyId,
        response.previous
      )
    }
    return this
  }

  async vote(currentWins: boolean) {
    const response = await this.client.annotatorVote(
      this.id,
      this.surveyId,
      currentWins
    )
    if (response.current) {
      this._current = await ItemInterface.createInterface(
        this.surveyId,
        response.current
      )
    }
    if (response.previous) {
      this._previous = await ItemInterface.createInterface(
        this.surveyId,
        response.previous
      )
    }
    return this
  }

  async delete() {
    return await this.client.deleteAnnotator(this.id, this.surveyId)
  }

  async patch(update: EditableAnnotator) {
    const self = await this.client.updateAnnotator(
      this.id,
      update,
      this.surveyId
    )
    return this.setSelf(self)
  }

  static async create(surveyId: SurveyId, data: NewAnnotator) {
    const annotator = await new PairwiseClient().createAnnotator(data, surveyId)
    return this.createInterface(surveyId, annotator)
  }

  static async createInterface(
    surveyId: SurveyId,
    self: Annotator
  ): Promise<Readonly<Annotator> & AnnotatorInterface>
  static async createInterface(
    surveyId: SurveyId,
    id: AnnotatorId
  ): Promise<Readonly<Annotator> & AnnotatorInterface>
  static async createInterface(
    surveyId: SurveyId,
    idOrSelf: AnnotatorId | Annotator
  ) {
    let annotator = idOrSelf
    if (typeof annotator === 'string') {
      annotator = await new PairwiseClient().getAnnotator(annotator, surveyId)
    }
    return new AnnotatorInterface(
      surveyId,
      annotator as Annotator
    ) as AnnotatorInterface & Annotator
  }
}

export class SurveyInterface extends BaseInterface<Survey> {
  protected async fetchSelf() {
    return await this.client.getSurvey(this.surveyId)
  }
  // private async *makeGenerator<T>(
  //   func: (id: SurveyId, page: number) => Promise<ListResponse<T>>,
  //   InterfaceConstructor: new (surveyId: SurveyId, self: T) => BaseInterface<T>
  // ) {
  //   let returnedCount = 0
  //   let page = 0
  //   let response = await func(this.surveyId, page)
  //   while (response.count >= returnedCount) {
  //     for (const result of response.results) {
  //       yield InterfaceConstructor.createInter(this.surveyId, result)
  //       returnedCount += 1
  //     }
  //     page += 1
  //     response = await func(this.surveyId, page)
  //   }
  // }

  // /**
  //  * Returns a generator of annotators
  //  */
  // getAnnotators() {
  //   return this.makeGenerator<Annotator>(
  //     this.client.getSurveyAnnotators,
  //     AnnotatorInterface
  //   )
  // }

  // /**
  //  * Returns a generator of items
  //  */
  // getItems() {
  //   return this.makeGenerator<Item>(this.client.getSurveyItems, ItemInterface)
  // }

  // /**
  //  * Returns a generator of ranked items
  //  */
  // getRanking() {
  //   return this.makeGenerator<Item>(this.client.getSurveyItems, ItemInterface)
  // }

  async delete() {
    return await this.client.deleteSurvey(this.surveyId)
  }

  async patch(update: EditableSurvey) {
    const self = await this.client.updateSurvey(this.surveyId, update)
    return this.setSelf(self)
  }

  createItem(data: NewItem) {
    return ItemInterface.create(this.surveyId, data)
  }

  createAnnotator(data: NewAnnotator) {
    return AnnotatorInterface.create(this.surveyId, data)
  }

  static async create(data: NewSurvey) {
    const survey = await new PairwiseClient().createSurvey(data)
    return this.createInterface(survey.id, survey)
  }

  static async createInterface(
    surveyId: SurveyId,
    self?: Survey
  ): Promise<Readonly<Survey> & SurveyInterface>
  static async createInterface(
    surveyId: SurveyId,
    self: Survey
  ): Promise<Readonly<Survey> & SurveyInterface>
  static async createInterface(
    surveyId: SurveyId,
    self?: Survey
  ): Promise<Readonly<Survey> & SurveyInterface> {
    let survey = self
    if (typeof survey === 'undefined') {
      survey = await new PairwiseClient().getSurvey(surveyId)
    }
    return new SurveyInterface(surveyId, survey) as SurveyInterface & Survey
  }
}
