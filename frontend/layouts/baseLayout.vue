<template>
  <v-app :dark="isDark">
    <v-navigation-drawer
      v-model="drawer"
      disable-resize-watcher
      class="d-md-none"
      :dark="!isDark"
      :light="isDark"
      app
    >
      <v-list>
        <v-list-item v-for="(item, i) in items" :key="i" :to="item.to" router exact>
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
        <v-list-item @click="toggleDark">
          <v-list-item-action>
            <v-icon>fas fa-check</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>dark mode</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <slot />
  </v-app>
</template>

<script lang="ts">
import { defineComponent, ref } from 'nuxt-composition-api'
import { provideToast } from 'vue-toastification/composition'
import 'vue-toastification/dist/index.css'
import { useDarkTheme } from '~/hooks/vuetify'
import { provideDrawer } from '~/hooks/app'

export default defineComponent({
  setup() {
    provideToast()
    const [drawer] = provideDrawer()
    const [isDark, toggleDark] = useDarkTheme()
    const items = ref([
      {
        icon: 'mdi-apps',
        title: 'Welcome',
        to: '/'
      },
      {
        icon: 'mdi-chart-bubble',
        title: 'Inspire',
        to: '/inspire'
      }
    ])
    return { drawer, items, isDark, toggleDark }
  }
})
</script>
