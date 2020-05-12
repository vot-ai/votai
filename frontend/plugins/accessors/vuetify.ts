import { Plugin } from '@nuxt/types'
import { initializeVuetify } from '~/utils/accessors'

const accessor: Plugin = ({ $vuetify }) => {
  initializeVuetify($vuetify)
}

export default accessor
