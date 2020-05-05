import { Module, VuexModule, Mutation } from 'vuex-module-decorators'

@Module({
  name: 'preferences',
  stateFactory: true,
  namespaced: true,
})
export default class Preferences extends VuexModule {
  language = 'pt-BR'

  @Mutation
  changeLanguage(language: string) {
    this.language = language
  }
}
