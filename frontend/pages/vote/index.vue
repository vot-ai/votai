<template>
  <v-container fill-height>
    <v-row align="center" justify="center">
      <fade-transition appear>
        <v-col cols="12" sm="8" md="6" lg="4">
          <h2 class="display-1 font-weight-light mb-3">{{$t('vote.header')}}</h2>
          <p class="body-1">{{$t('vote.body')}}</p>
        </v-col>
      </fade-transition>
      <fade-transition appear>
        <v-col cols="12">
          <v-row align="center" justify="center">
            <v-col cols="8" sm="6" md="3" lg="2" align-self="start">
              <search-survey-input auto-navigate />
            </v-col>
          </v-row>
        </v-col>
      </fade-transition>
    </v-row>
  </v-container>
</template>
<script lang="ts">
import { defineComponent } from '@vue/composition-api'
import SearchSurveyInput from '~/components/forms/SearchSurveyInput.vue'

export default defineComponent({
  ...{ auth: false },
  components: { SearchSurveyInput }
})
</script>
