<template>
  <v-text-field
    v-model="state.search"
    v-mask="'XXXXXXXXXXXX'"
    clear-icon="fas fa-times"
    solo
    flat
    outlined
    clearable
    :loading="state.loading"
    :disabled="state.loading"
    autofocus
    counter="12"
    :placeholder="$t('search-survey-input.placeholder')"
    :error-messages="state.valid ? undefined : state.error"
  />
</template>

<script>
import {
  defineComponent,
  reactive,
  computed,
  watch
} from '@vue/composition-api'
import { useI18n } from '~/hooks/i18n'
import { useAuth } from '~/hooks/auth'

export default defineComponent({
  props: {
    idLength: {
      type: Number,
      default: 12
    },
    autoNavigate: {
      type: Boolean,
      default: false
    }
  },
  setup({ idLength, autoNavigate }, ctx) {
    const auth = useAuth()
    const i18n = useI18n()
    const errorMessage = computed(() =>
      i18n.t('search-survey-input.survey-not-found-error')
    )
    const state = reactive({
      search: '',
      loading: false,
      valid: true,
      error: errorMessage
    })
    const canSearch = computed(() => {
      return state.search && state.search.length === idLength
    })
    watch([() => state.search], () => {
      ctx.emit('input', false)
      state.valid = true
      if (canSearch.value) {
        state.loading = true
        auth
          .request({
            url: `/api/survey/${state.search}`
          })
          .then(() => {
            ctx.emit('input', state.search)
            if (autoNavigate) {
              ctx.root.$router.push(`/vote/${state.search}`)
            }
          })
          .catch(() => {
            state.valid = false
          })
          .finally(() => {
            state.loading = false
          })
      }
    })

    return { state, canSearch }
  }
})
</script>
