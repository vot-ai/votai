import { reactive, onBeforeMount } from '@vue/composition-api'

export const useFetchData = (callback: () => Promise<void>) => {
  const fetchState = reactive({
    pending: true,
    error: null as Error | null
  })
  const fetch = async () => {
    fetchState.pending = true
    fetchState.error = null
    try {
      await callback()
    } catch (e) {
      fetchState.error = e
    } finally {
      fetchState.pending = false
    }
  }
  onBeforeMount(fetch)
  return [fetch, fetchState] as [typeof fetch, typeof fetchState]
}
