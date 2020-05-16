import {
  computed,
  reactive,
  provide,
  inject,
  watch,
  getCurrentInstance
} from '@vue/composition-api'
import { useAuthStorage } from './auth'

export const useDarkTheme = () => {
  const [theme, setTheme] = useAuthStorage('theme', { dark: false })
  const instance = getCurrentInstance()
  watch(
    () => theme.value.dark,
    dark => {
      if (instance) {
        instance.$vuetify.theme.dark = dark
      }
    }
  )
  const isDark = computed(() => {
    return theme.value.dark
  })
  const toggleDark = () => setTheme({ dark: !theme.value.dark })
  const setDark = (dark: boolean) => setTheme({ dark })
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
  const setTheme = (isDark: boolean) => {
    localTheme.isDark = isDark
  }
  const toggleTheme = () => {
    setTheme(!localTheme.isDark)
  }
  watch(
    () => injectedTheme.isDark,
    isDark => {
      setTheme(!isDark)
    }
  )
  provide('theme', localTheme)

  return [setTheme, toggleTheme] as [typeof setTheme, typeof toggleTheme]
}
