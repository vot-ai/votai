import { Store } from 'vuex'
import { getModule } from 'vuex-module-decorators'
import preferences from '~/store/preferences'

// eslint-disable-next-line import/no-mutable-exports
let preferencesStore: preferences

function initialiseStores(store: Store<any>): void {
  preferencesStore = getModule(preferences, store)
}

export { initialiseStores, preferencesStore }
