<template>
  <content-container>
    <fade-transition appear group>
      <div v-if="fetchState.pending" key="skeletons">
        <v-skeleton-loader class="mt-5" tile type="heading"></v-skeleton-loader>
        <v-skeleton-loader class="mt-5" tile type="paragraph"></v-skeleton-loader>
        <v-skeleton-loader class="mt-3" tile type="chip"></v-skeleton-loader>
      </div>
      <div v-else-if="fetchState.error" key="error">
        <h1 key="error" class="display-2 font-weight-thin my-5">{{$t('vote.survey-not-found')}}</h1>
      </div>
      <div v-else-if="state.survey" key="content">
        <h1 class="display-2 font-weight-thin my-5">{{ state.survey.name }}</h1>
        <h3 class="subtitle-1 ml-2 font-weight-light">
          Survey's ID:
          <v-tooltip
            top
            :nudge-left="state.copied * 6"
            :close-delay="state.copied ? 2500 : undefined"
          >
            <template v-slot:activator="{ on }">
              <kbd class="survey-id my-5" v-on="on" @click="copySurveyId">{{ state.survey.id }}</kbd>
            </template>
            <span v-if="!state.copied">Copy ID</span>
            <span v-else>ID copied!</span>
          </v-tooltip>
        </h3>
        <fade-transition group>
          <!-- The user is not authenticated -->
          <div v-if="!$auth.loggedIn" key="not-logged">
            <v-row align="center" justify="center">
              <v-col cols="12" md="6">
                <v-alert color="red" outlined>{{$t('vote.requires-auth')}}</v-alert>
              </v-col>
            </v-row>
            <login-buttons redirect :hide-anon="!state.survey.allowAnon" />
          </div>
          <!-- The user is authenticated as anon, but the survey does not allow anons -->
          <div
            v-else-if="$auth.strategy.name === 'anonymous' && !state.survey.allowAnon"
            key="not-logged"
          >
            <v-row align="center" justify="center">
              <v-col cols="12" md="6">
                <v-alert color="red" outlined>{{$t('vote.requires-registered-auth')}}</v-alert>
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
          <!-- User has access -->
          <div v-else key="menu">
            <annotator-menu :survey="state.survey" />
          </div>
        </fade-transition>
      </div>
    </fade-transition>
  </content-container>
</template>

<script lang="ts">
import { defineComponent, reactive, useContext } from 'nuxt-composition-api'
import { useAuth } from '~/hooks/auth'
import { useClipboard } from '~/hooks/clipboard'
import { useFetchData } from '~/hooks/fetch'
import ContentContainer from '~/components/layouts/ContentContainer.vue'
import LoginButtons from '~/components/login/LoginButtons.vue'
import PasswordInput from '~/components/vote/PasswordInput.vue'
import AnnotatorMenu from '~/components/vote/AnnotatorMenu.vue'
import { SerializedSurvey } from '~/types/survey'

export default defineComponent({
  components: { ContentContainer, LoginButtons, PasswordInput, AnnotatorMenu },
  head: {},
  setup() {
    const { params } = useContext()
    const auth = useAuth()
    const copyText = useClipboard()
    const state = reactive({
      survey: null as SerializedSurvey | null,
      copied: false
    })
    const [fetch, fetchState] = useFetchData(async () => {
      const response = await auth.request({
        url: `/api/survey/${params.survey}`
      })
      state.survey = response.data
    })

    const reloadSuvey = (isValid: boolean) => {
      if (isValid) {
        fetch()
      }
    }

    const copySurveyId = () => {
      copyText(state.survey?.id || '')
        .then(() => {
          state.copied = true
        })
        .then(
          () =>
            new Promise(resolve =>
              setTimeout(() => {
                state.copied = false
                resolve()
              }, 3000)
            )
        )
    }
    return { state, reloadSuvey, copySurveyId, fetch, fetchState }
  },
  ...{ auth: false }
})
</script>
<style lang="scss" scoped>
.survey-id {
  cursor: pointer;
}
</style>
