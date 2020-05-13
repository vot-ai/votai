<template>
  <div>
    <index-banner />
    <v-container>
      <v-row justify="center" align-center>
        <v-col xs="12" lg="10" xl="8" class="d-flex">hey</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
        <v-col xs="12" sm="10" md="8">content here</v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'nuxt-composition-api'
import { useToast } from 'vue-toastification/composition'

import IndexBanner from '~/components/index/IndexBanner.vue'

export default defineComponent({
  ...{ auth: false },
  name: 'Index',
  layout: 'firstPage',
  components: {
    IndexBanner
  },
  setup() {
    const toast = useToast()
    return { toast }
  },
  methods: {
    localeChange() {
      if (this.$i18n.locale === 'pt') {
        this.$i18n.setLocale('en')
      } else {
        this.$i18n.setLocale('pt')
      }
    }
  }
})
</script>
