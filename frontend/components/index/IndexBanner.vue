<template>
  <div class="banner">
    <v-container fluid class="pa-0">
      <v-row no-gutters align="stretch" justify="center" class="first-row">
        <v-col md="6" cols="12" class="pa-0">
          <v-sheet tile elevation="0" height="100%">
            <fade-transition appear leave>
              <v-row no-gutters class="d-none d-md-block some-margin">
                <v-col cols="12" class="text-right">
                  <h1 class="display-3">{{$t('index.headerPt1')}}</h1>
                </v-col>
              </v-row>
            </fade-transition>
            <fade-transition appear leave>
              <v-row no-gutters align="center" justify="space-around" class="content">
                <v-col cols="12" class="text-center" align-self="end">
                  <h2 class="display-1 font-weight-light">{{$t('index.join-survey')}}</h2>
                </v-col>
                <v-col cols="8" md="4" align-self="start" class="mt-5">
                  <search-survey auto-navigate />
                </v-col>
              </v-row>
            </fade-transition>
          </v-sheet>
        </v-col>
        <v-col md="6" cols="12" class="pa-0">
          <i-sheet tile elevation="0" height="100%">
            <fade-transition appear>
              <v-row no-gutters class="d-none d-md-block some-margin">
                <v-col cols="12" class="text-left">
                  <h1 class="display-3">{{$t('index.headerPt2')}}</h1>
                </v-col>
              </v-row>
            </fade-transition>
            <fade-transition appear>
              <v-row no-gutters align="center" justify="center" class="content">
                <v-col cols="12" class="text-center" align-self="end">
                  <h2 class="display-1 font-weight-light">{{$t('index.create-survey')}}</h2>
                </v-col>
                <v-col cols="8" md="4" align-self="start" class="mt-5 mb-5 pb-3 text-center">
                  <i-btn
                    tile
                    depressed
                    x-large
                    nuxt
                    to="/create"
                  >{{$t('index.create-survey-button')}}</i-btn>
                </v-col>
              </v-row>
            </fade-transition>
          </i-sheet>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'
import SearchSurvey from '~/components/forms/SearchSurveyInput.vue'
export default defineComponent({
  components: { SearchSurvey }
})
</script>

<style lang="scss" scoped>
.some-margin {
  margin-top: 10vh;
}
</style>

<style lang="scss" scoped>
.banner {
  .content {
    height: 100%;
    @media #{map-get($display-breakpoints, 'md-and-up')} {
      height: 70%;
    }
  }
  .theme--dark {
    background-color: map-get($map: $material-dark, $key: background);
  }
  .container {
    height: 100vh;
    .first-row {
      height: 100%;
      @media #{map-get($display-breakpoints, 'sm-and-down')} {
        padding-top: 80px;
      }
      .v-sheet {
        @media #{map-get($display-breakpoints, 'md-and-up')} {
          padding-top: 80px;
        }
      }
    }
  }
}
</style>
