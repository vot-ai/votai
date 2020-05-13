<template>
  <v-form v-model="state.valid" @submit.prevent>
    <v-row class="my-3 text-center">
      <v-col align-self="center">
        <v-text-field
          v-model="state.password"
          type="password"
          clear-icon="fas fa-times"
          solo
          flat
          outlined
          clearable
          :loading="state.loading"
          :disabled="state.loading"
          autofocus
          maxlength="50"
          :placeholder="$t('login.password-input.placeholder')"
          :error-messages="state.valid ? undefined : state.error"
        />
        <v-btn
          :loading="state.loading"
          :disabled="!canValidate"
          tile
          depressed
          type="submit"
          @click="validate"
        >{{$t('login.password-input.submit')}}</v-btn>
      </v-col>
    </v-row>
  </v-form>
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
    surveyId: {
      type: String,
      required: true
    }
  },
  setup({ surveyId }, ctx) {
    const auth = useAuth()
    const i18n = useI18n()
    const errorMessage = computed(() =>
      i18n.t('login.password-input.wrong-password')
    )
    const state = reactive({
      password: '',
      loading: false,
      valid: true,
      error: errorMessage
    })
    const canValidate = computed(() => {
      return state.password && state.password.length >= 6
    })
    watch([() => state.password], () => {
      state.valid = true
    })
    const validate = () => {
      ctx.emit('validate', false)
      state.loading = true
      auth
        .request({
          method: 'POST',
          url: `/api/survey/${surveyId}/access`,
          data: {
            password: state.password
          }
        })
        .then(() => {
          ctx.emit('validate', true)
        })
        .catch(() => {
          state.valid = false
        })
        .finally(() => {
          state.loading = false
        })
    }
    return { state, canValidate, validate }
  }
})
</script>
