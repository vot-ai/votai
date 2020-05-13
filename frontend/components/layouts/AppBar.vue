<template>
  <v-app-bar v-bind="$attrs" hide-on-scroll elevate-on-scroll app height="80" v-on="$listeners">
    <v-app-bar-nav-icon class="d-md-none" @click.stop="toggleDrawer" />
    <v-container class="pa-0">
      <v-row justify="center" align="center" no-gutters>
        <v-col xs="12" lg="10" xl="8">
          <v-row align="center">
            <v-spacer class="d-md-none" />
            <v-col cols="auto">
              <v-toolbar-title class="logo" @click="$router.push('/')">votAI</v-toolbar-title>
            </v-col>
            <v-spacer class="d-none d-md-block" />
            <v-col
              v-for="item in items"
              :key="item.text"
              cols="auto"
              class="pa-0 d-none d-md-block"
            >
              <template v-if="item.to">
                <v-btn tile depressed text :to="item.to" nuxt>{{ item.text }}</v-btn>
              </template>
              <template v-if="item.onClick">
                <v-btn tile depressed text @click="item.onClick()">{{ item.text }}</v-btn>
              </template>
            </v-col>
            <v-col cols="auto" class="pa-0 d-none d-md-block">
              <v-menu offset-y left>
                <template v-slot:activator="{ on }">
                  <v-btn
                    tile
                    depressed
                    text
                    v-on="on"
                  >{{ getFlag($i18n.locale) }} {{ $i18n.locale }}</v-btn>
                </template>
                <v-list>
                  <v-list-item
                    v-for="(locale, index) in locales"
                    :key="index"
                    :input-value="locale.code === $i18n.locale"
                    @click="setLocale(locale.code)"
                  >
                    <v-list-item-title>
                      {{ getFlag(locale.code) }}
                      <span class="ml-2">{{ getLocaleName(locale.code) }}</span>
                    </v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<script lang="ts">
import { defineComponent, computed } from 'nuxt-composition-api'
import { useDrawer } from '~/hooks/app'
import { useInvertedTheme, useDarkTheme } from '~/hooks/vuetify'
import { useAuth } from '~/hooks/auth'
import { useI18n } from '~/hooks/i18n'

export default defineComponent({
  setup() {
    useInvertedTheme()
    const [, toggleDrawer] = useDrawer()
    const auth = useAuth()
    const i18n = useI18n()
    const [dark, toggleDark] = useDarkTheme()
    const flags = { en: '🇺🇸', pt: '🇧🇷' }
    const localeNames = { en: 'English', pt: 'Português' }
    const getFlag = <T extends keyof typeof flags>(key: T) => flags[key]
    const getLocaleName = <T extends keyof typeof localeNames>(key: T) =>
      localeNames[key]
    const setLocale = (key: string) => i18n.setLocale(key)
    const locales = i18n.locales

    const items = computed(() => {
      const baseItems: { text: string; to?: string; onClick?: () => any }[] = [
        {
          text: i18n.t('app-bar.about').toString(),
          to: '/about'
        },
        {
          text: i18n.t('app-bar.create').toString(),
          to: '/create'
        },
        {
          text: i18n.t('app-bar.vote').toString(),
          to: '/vote'
        },
        {
          text: dark.value
            ? i18n.t('app-bar.light-theme').toString()
            : i18n.t('app-bar.dark-theme').toString(),
          onClick: toggleDark
        }
      ]
      if (auth.loggedIn) {
        baseItems.push({
          text: i18n.t('app-bar.you').toString(),
          to: '/me'
        })
        baseItems.push({
          text: i18n.t('logout').toString(),
          onClick: () => auth.logout()
        })
      } else {
        baseItems.push({
          text: i18n.t('login-button').toString(),
          to: '/login'
        })
      }
      return baseItems
    })

    return { toggleDrawer, items, locales, getFlag, setLocale, getLocaleName }
  }
})
</script>

<style scoped>
.logo {
  font-family: 'Major Mono Display', monospace;
  font-size: 3rem;
  cursor: pointer;
}
</style>
