import { Plugin } from '@nuxt/types'
import { initializeAuth } from '~/utils/accessors'

const accessor: Plugin = ({ $auth }) => {
  initializeAuth($auth)
}

export default accessor
