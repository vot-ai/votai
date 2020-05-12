import { Plugin } from '@nuxt/types'
import vuetify from './vuetify'
import axios from './axios'

const accessor: Plugin = (ctx, inject) => {
  vuetify(ctx, inject)
  axios(ctx, inject)
}

export default accessor
