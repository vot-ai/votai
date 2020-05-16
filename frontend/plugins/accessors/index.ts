import { Plugin } from '@nuxt/types'
import vuetify from './vuetify'
import axios from './axios'
import auth from './auth'

const accessor: Plugin = (ctx, inject) => {
  vuetify(ctx, inject)
  axios(ctx, inject)
  auth(ctx, inject)
}

export default accessor
