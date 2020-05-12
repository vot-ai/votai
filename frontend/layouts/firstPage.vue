<template>
  <base-layout>
    <app-bar v-scroll="onScroll" :color="transparentColor" />
    <v-content>
      <nuxt />
    </v-content>
  </base-layout>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'nuxt-composition-api'
import BaseLayout from './baseLayout.vue'
import AppBar from '~/components/layouts/AppBar.vue'

export default defineComponent({
  layout: 'empty',
  components: { BaseLayout, AppBar },
  setup() {
    const scrolled = ref(false)
    const onScroll = () => {
      if (window.scrollY > 0) {
        scrolled.value = true
      } else {
        scrolled.value = false
      }
    }

    const transparentColor = computed(() =>
      !scrolled.value ? 'transparent' : undefined
    )
    return {
      onScroll,
      transparentColor
    }
  }
})
</script>

<style scoped>
.logo {
  font-family: 'Major Mono Display', monospace;
  font-size: 3rem;
}
</style>
<style>
.v-content {
  padding-top: 0px !important;
}
</style>
