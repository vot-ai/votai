<template>
  <fade-transition enter leave appear>
    <v-row v-if="fetchState.pending" key="skeletons" justify="center" align="center">
      <v-col cols="12" sm="6" md="4">
        <v-skeleton-loader tile type="image, card-heading, list-item-three-line, actions"></v-skeleton-loader>
      </v-col>
      <v-col cols="12" sm="6" md="4">
        <v-skeleton-loader tile type="image, card-heading, list-item-three-line, actions"></v-skeleton-loader>
      </v-col>
    </v-row>
    <v-row v-else-if="fetchState.error" key="error" justify="center" align="center">
      <v-col cols="12" sm="6" md="4" align-self="center" class="text-center">
        <h2 class="display-1 font-weight-light my-5">{{$t('vote.annotator-menu.loading-error')}}</h2>
        <i-btn tile @click="fetch">{{$t('vote.annotator-menu.loading-error-try-again')}}</i-btn>
      </v-col>
    </v-row>
    <v-row
      v-else-if="!state.annotator.current && !state.annotator.previous"
      key="no-assigned"
      justify="center"
      align="center"
    >
      <v-col cols="12" sm="6" md="4" align-self="center" class="text-center">
        <h2
          class="display-1 font-weight-light my-5"
        >{{$t('vote.annotator-menu.no-assigned-choices.header')}}</h2>
        <p class="body-2">{{$t('vote.annotator-menu.no-assigned-choices.description')}}</p>
        <i-btn tile @click="fetch">{{$t('vote.annotator-menu.no-assigned-choices.reload-button')}}</i-btn>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col cols="12">
        <v-row justify="center" align="center">
          <v-col class="text-center" cols="12">
            <h3
              class="overline"
            >{{$tc('vote.annotator-menu.voting.comparisons-counter', state.annotator.itemsLeft)}}</h3>
          </v-col>
        </v-row>
        <transition-group name="list" tag="div" class="row align-center justify-center">
          <v-col
            v-if="state.annotator.current"
            :key="state.annotator.current.id"
            cols="12"
            sm="6"
            md="4"
            align-self="start"
          >
            <annotator-item
              current
              :item="state.annotator.current"
              :even="state.counter % 2 === 0"
              :first="!state.annotator.previous"
              :loading="state.loading"
              @selected="vote(true)"
            />
          </v-col>
          <v-col
            v-if="state.annotator.previous"
            :key="state.annotator.previous.id"
            cols="12"
            sm="6"
            md="4"
            align-self="start"
          >
            <annotator-item
              :item="state.annotator.previous"
              :even="state.counter % 2 === 0"
              :waiting="!state.annotator.current"
              :last="state.annotator.itemsLeft === 0"
              :loading="state.loading"
              @selected="vote(false)"
            />
          </v-col>
        </transition-group>
        <v-row justify="center" align="center">
          <v-col class="text-center" cols="12">
            <v-btn
              x-large
              text
              :loading="state.loading"
              :disabled="!state.annotator.current || !state.annotator.previous"
              @click="skip()"
            >{{$t('vote.annotator-menu.skip-button')}}</v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </fade-transition>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from '@vue/composition-api'
import { useToast } from 'vue-toastification/composition'
import AnnotatorItem from './AnnotatorItem.vue'
import { SerializedSurvey, SerializedAnnotator } from '~/types/survey'
import { useAuth } from '~/hooks/auth'
import { useI18n } from '~/hooks/i18n'
import { useFetchData } from '~/hooks/fetch'

export default defineComponent({
  components: { AnnotatorItem },
  props: {
    survey: {
      type: Object as () => SerializedSurvey,
      required: true
    }
  },
  setup(props) {
    const auth = useAuth()
    const toast = useToast()
    const i18n = useI18n()
    const state = reactive({
      annotator: null as SerializedAnnotator | null,
      loading: false
    })

    const counter = ref(0)
    const increaseCounter = () => counter.value++

    const [fetch, fetchState] = useFetchData(async () => {
      const response = await auth.request({
        url: `/api/survey/${props.survey.id}/annotator`
      })
      state.annotator = response.data
    })

    const vote = async (currentWins: boolean) => {
      state.loading = true
      await auth
        .request({
          method: 'POST',
          url: `/api/survey/${props.survey.id}/annotator/vote`,
          data: {
            currentWins
          }
        })
        .then(response => {
          state.annotator = response.data
          increaseCounter()
        })
        .catch(() => {
          toast.error(i18n.t('vote.vote-action.error'))
        })
        .finally(() => {
          state.loading = false
        })
    }

    const skip = async () => {
      state.loading = true
      await auth
        .request({
          method: 'POST',
          url: `/api/survey/${props.survey.id}/annotator/skip`
        })
        .then(response => {
          state.annotator = response.data
          increaseCounter()
        })
        .catch(() => {
          toast.error(i18n.t('vote.skip-action.error'))
        })
        .finally(() => {
          state.loading = false
        })
    }

    return { state, skip, vote, counter, fetch, fetchState }
  }
})
</script>

<style lang="scss" scoped>
.list-move {
  transition: transform 1s;
}
.list-enter-active {
  transition: all 2s;
}
.list-leave-active {
  transition: all 0s;
  position: absolute;
  opacity: 0;
}
.list-enter {
  opacity: 0;
}
</style>