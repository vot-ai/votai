import {
  computed,
  reactive,
  provide,
  inject,
  watch,
  getCurrentInstance
} from '@vue/composition-api'
import { preferencesStore } from '~/store'

export const useDarkTheme = () => {
  const isDark = computed(() => {
    const dark = preferencesStore.dark
    const instance = getCurrentInstance()
    if (instance) {
      instance.$vuetify.theme.dark = dark
    }
    return dark
  })
  const toggleDark = preferencesStore.toggleDark
  const setDark = preferencesStore.changeDark
  return [isDark, toggleDark, setDark] as [
    typeof isDark,
    typeof toggleDark,
    typeof setDark
  ]
}

export const useInvertedTheme = () => {
  const injectedTheme = inject('theme') as { isDark: boolean }
  const localTheme = reactive({
    isDark: !injectedTheme.isDark
  })
  watch(
    () => injectedTheme.isDark,
    isDark => {
      localTheme.isDark = !isDark
    }
  )
  provide('theme', localTheme)
}
