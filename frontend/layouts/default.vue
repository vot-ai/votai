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
import BaseLayout from './baseLayout.vue'
import AppBar from '~/components/layouts/AppBar.vue'

export default defineComponent({
  layout: 'empty',
  components: { BaseLayout, AppBar }
})
</script>
