import { getCurrentInstance } from '@vue/composition-api'

type NotNull<T> = T extends undefined ? never : T

export const useI18n = () => {
  const i18n = getCurrentInstance()?.$i18n
  if (i18n) {
    return i18n
  }
  return {} as NotNull<typeof i18n>
}
