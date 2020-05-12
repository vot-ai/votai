import { ref, provide, inject, InjectionKey } from '@vue/composition-api'

const loadDrawer = () => {
  const isOpen = ref(false)
  const toggleDrawer = () => {
    isOpen.value = !isOpen.value
  }
  const hook = [isOpen, toggleDrawer] as [typeof isOpen, typeof toggleDrawer]
  return hook
}

export const provideDrawer = () => {
  const hook = loadDrawer()
  provide(Drawer, hook)
  return hook
}

const Drawer: InjectionKey<ReturnType<typeof provideDrawer>> = Symbol('dawer')

export const useDrawer = () => {
  const hook = inject(Drawer, loadDrawer())
  return hook
}
