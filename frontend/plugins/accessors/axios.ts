import { Plugin } from '@nuxt/types'
import { initializeAxios } from '~/utils/accessors'

const accessor: Plugin = ({ $axios }) => {
  initializeAxios($axios)
}

export default accessor
