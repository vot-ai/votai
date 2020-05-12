import { Store } from 'vuex'
import { initialiseStores } from '~/utils/accessors'

const initializer = (store: Store<any>) => initialiseStores(store)

export const plugins = [initializer]
export * from '~/utils/accessors/store'
