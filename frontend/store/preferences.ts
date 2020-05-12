import { Module, VuexModule, Mutation } from 'vuex-module-decorators'

@Module({
  name: 'preferences',
  stateFactory: true,
  namespaced: true
})
export default class Preferences extends VuexModule {
  dark = false

  @Mutation
  changeDark(mode: boolean) {
    this.dark = mode
  }

  @Mutation
  toggleDark() {
    this.dark = !this.dark
  }
}
