<template>
  <content-container>
    <fade-transition enter leave appear>
      <div v-if="$fetchState.pending" key="skeletons">
        <v-skeleton-loader class="mt-5" tile type="article"></v-skeleton-loader>
        <v-skeleton-loader class="mt-5" tile type="heading"></v-skeleton-loader>
      </div>
      <div v-else-if="$fetchState.error" key="error">
        <h1 key="error" class="display-2 font-weight-thin my-5">{{$t('vote.survey-not-found')}}</h1>
      </div>
      <div v-else key="content">
        <h1 class="display-2 font-weight-thin my-5">{{ state.survey.name }}</h1>
        <fade-transition enter leave>
          <!-- The user is not authenticated -->
          <div v-if="!$auth.loggedIn" key="not-logged">
            <v-row align="center" justify="center">
              <v-col cols="12" md="6">
                <v-alert color="red" outlined>{{$t('vote.requires-auth')}}</v-alert>
              </v-col>
            </v-row>
            <login-buttons redirect :hide-anon="!state.survey.allowAnon" />
          </div>
          <!-- Survey has a password and the user does not have access -->
          <div
            v-else-if="state.survey.private && typeof state.survey.active === 'undefined'"
            key="password"
          >
            <v-row align="center" justify="center">
              <v-col cols="12" md="6">
                <v-alert color="red" outlined>{{$t('vote.requires-password')}}</v-alert>
              </v-col>
            </v-row>
            <v-row align="center" justify="center">
              <v-col cols="12" md="6">
                <password-input :survey-id="state.survey.id" @validate="reloadSuvey" />
              </v-col>
            </v-row>
          </div>
        </fade-transition>
      </div>
    </fade-transition>
  </content-container>
</template>

<script lang="ts">
import {
  defineComponent,
  useFetch,
  reactive,
  useContext
} from 'nuxt-composition-api'
import { useAuth } from '~/hooks/auth'
import ContentContainer from '~/components/layouts/ContentContainer.vue'
import LoginButtons from '~/components/login/LoginButtons.vue'
import PasswordInput from '~/components/vote/PasswordInput.vue'

export default defineComponent({
  components: { ContentContainer, LoginButtons, PasswordInput },
  setup() {
    const { params } = useContext()
    const auth = useAuth()
    const state = reactive({
      survey: null as any
    })
    const { $fetch } = useFetch(async () => {
      const response = await auth.request({
        url: `/api/survey/${params.survey}`
      })
      state.survey = response.data
    })

    const reloadSuvey = (isValid: boolean) => {
      if (isValid) {
        $fetch()
      }
    }

    return { state, reloadSuvey }
  },
  ...{ auth: false }
})
</script>
