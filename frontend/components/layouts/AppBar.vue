<template>
  <v-app-bar
    v-bind="$attrs"
    hide-on-scroll
    scroll-threshold="80"
    elevate-on-scroll
    app
    height="80"
    v-on="$listeners"
  >
    <v-app-bar-nav-icon class="d-md-none" @click.stop="toggleDrawer" />
    <v-container class="pa-0">
      <v-row justify="center" align-center>
        <v-col xs="12" sm="10" md="8" class="d-flex">
          <v-spacer class="d-md-none" />
          <v-toolbar-title class="logo">votAI</v-toolbar-title>
        </v-col>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<script lang="ts">
import { defineComponent } from 'nuxt-composition-api'
import { useDrawer } from '../../hooks/app'

export default defineComponent({
  setup() {
    const [, toggleDrawer] = useDrawer()
    return { toggleDrawer }
  }
})
</script>

<style scoped>
.logo {
  font-family: 'Major Mono Display', monospace;
  font-size: 3rem;
}
</style>
