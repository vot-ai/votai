import { getCurrentInstance } from '@vue/composition-api'

export const useClipboard = () => {
  const instance = getCurrentInstance() as NonNullable<
    ReturnType<typeof getCurrentInstance>
  >
  return instance.$copyText
}
