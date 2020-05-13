<template>
  <v-app :dark="isDark">
    <nav-drawer />
    <slot />
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'nuxt-composition-api'
import { provideToast } from 'vue-toastification/composition'
import 'vue-toastification/dist/index.css'

import { useDarkTheme } from '~/hooks/vuetify'
import { provideDrawer } from '~/hooks/app'
import NavDrawer from '~/components/layouts/NavDrawer.vue'

export default defineComponent({
  name: 'BaseLayout',
  components: { NavDrawer },
  setup() {
    provideToast()
    provideDrawer()
    const [isDark] = useDarkTheme()
    return { isDark }
  }
})
</script>
