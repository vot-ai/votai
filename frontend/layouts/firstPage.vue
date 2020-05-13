<template>
  <base-layout>
    <app-bar />
    <v-content>
      <nuxt />
    </v-content>
  </base-layout>
</template>

<script lang="ts">
import { defineComponent } from 'nuxt-composition-api'
import BaseLayout from './BaseLayout.vue'
import AppBar from '~/components/layouts/AppBar.vue'

export default defineComponent({
  name: 'FirstPage',
  layout: 'empty',
  components: { BaseLayout, AppBar }
})
</script>

<style scoped>
.v-content {
  padding-top: 0px !important;
}
</style>
