import { getCurrentInstance } from '@vue/composition-api'
import { Auth } from '@nuxtjs/auth-next/dist/types'

export const useAuth = () => {
  const instance = getCurrentInstance()
  if (instance) {
    return instance.$auth
  }
  return {} as Auth
}
