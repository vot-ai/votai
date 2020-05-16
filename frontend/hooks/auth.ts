import { getCurrentInstance, ref, watch, Ref } from '@vue/composition-api'
import { Auth } from '@nuxtjs/auth-next/dist/types'

export const useAuth = () => {
  const instance = getCurrentInstance()
  if (instance) {
    return instance.$auth
  }
  return {} as Auth
}

export const useAuthStorage = <T extends {}>(key: string, initialValue: T) => {
  const storage = useAuth().$storage
  const getUniversalState = (): T | undefined => storage.getUniversal(key)
  const setUniversalState = (value: T) => {
    storage.setUniversal(key, value)
  }
  const stateRef: Ref<T> = ref(getUniversalState() || initialValue)

  // Sync state changes with storage
  watch(stateRef, newState => {
    setUniversalState(newState)
  })

  const setState = (newState: Partial<T>) => {
    stateRef.value = { ...stateRef.value, ...newState }
  }

  return [stateRef, setState] as [Ref<Readonly<T>>, typeof setState]
}
