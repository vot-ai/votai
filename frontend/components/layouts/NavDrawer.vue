<template>
  <v-navigation-drawer
    v-model="drawer"
    disable-resize-watcher
    class="d-md-none"
    :dark="!isDark"
    :light="isDark"
    app
  >
    <template v-if="$auth.loggedIn">
      <v-list-item class="my-3" @click="$router.push('/me')">
        <template v-if="$auth.strategy.name === 'anonymous'">
          <v-list-item-content>
            <v-list-item-title>{{ $t('nav-drawer.anonymous') }}</v-list-item-title>
            <v-list-item-subtitle>{{ $auth.user.uuid }}</v-list-item-subtitle>
          </v-list-item-content>
        </template>
        <template v-else>
          <v-list-item-avatar>
            <img :src="$auth.user.picture" />
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title>{{ $auth.user.name }}</v-list-item-title>
            <v-list-item-subtitle>{{ $auth.user.email }}</v-list-item-subtitle>
          </v-list-item-content>
        </template>
      </v-list-item>
    </template>
    <v-divider />
    <v-list>
      <template v-for="(item, i) in items">
        <v-list-item v-if="item.to" :key="i" class="capitalize" :to="item.to" router>
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
        <v-list-item
          v-if="item.onClick"
          :key="i"
          class="capitalize"
          :to="item.to"
          @click="item.onClick"
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-list>
    <template v-slot:append>
      <v-divider />
      <v-list class="capitalize">
        <v-list-group class="inverted-list-item" append-icon>
          <template v-slot:activator>
            <v-list-item-action>
              <h2>{{ getFlag($i18n.locale) }}</h2>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>{{$t('language')}}</v-list-item-title>
            </v-list-item-content>
          </template>

          <v-list-item
            v-for="(locale, i) in locales"
            :key="i"
            class="ml-5"
            @click="setLocale(locale.code)"
          >
            <v-list-item-action>
              <h2>{{ getFlag(locale.code) }}</h2>
            </v-list-item-action>
            <v-list-item-title>{{ getLocaleName(locale.code) }}</v-list-item-title>
          </v-list-item>
          <v-divider />
        </v-list-group>
        <v-list-item @click="toggleDark">
          <v-list-item-action>
            <v-icon>fas fa-adjust</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ isDark ? $t('app-bar.light-theme') : $t('app-bar.dark-theme') }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <div class="pa-2">
        <i-btn v-if="$auth.loggedIn" block tile depressed @click="$auth.logout()">{{$t('logout')}}</i-btn>
        <i-btn v-else block tile depressed to="/login" nuxt>{{$t('login-button')}}</i-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script lang="ts">
import { defineComponent, computed } from 'nuxt-composition-api'
import { useDarkTheme } from '~/hooks/vuetify'
import { useDrawer } from '~/hooks/app'
import { useI18n } from '~/hooks/i18n'

export default defineComponent({
  setup() {
    const [drawer] = useDrawer()
    const [isDark, toggleDark] = useDarkTheme()
    const i18n = useI18n()
    const flags = { en: '🇺🇸', pt: '🇧🇷' }
    const localeNames = { en: 'English', pt: 'Português' }
    const getFlag = <T extends keyof typeof flags>(key: T) => flags[key]
    const getLocaleName = <T extends keyof typeof localeNames>(key: T) =>
      localeNames[key]
    const setLocale = (key: string) => i18n.setLocale(key)
    const locales = i18n.locales
    const items = computed(() => [
      {
        icon: 'fas fa-plus',
        title: i18n.t('app-bar.create'),
        to: '/create'
      },
      {
        icon: 'fas fa-vote-yea',
        title: i18n.t('app-bar.vote'),
        to: '/vote'
      },
      {
        icon: 'fas fa-info-circle',
        title: i18n.t('app-bar.about'),
        to: '/about'
      }
    ])
    return {
      drawer,
      items,
      isDark,
      toggleDark,
      locales,
      setLocale,
      getFlag,
      getLocaleName
    }
  }
})
</script>
<style lang="scss" scoped>
.v-list-item__action {
  margin: 0px;
  width: 40px;
  justify-content: center;
  margin-right: 20px !important;
  .theme--light {
    color: map-get($map: $material-dark, $key: background);
  }
}
.capitalize {
  .v-list-item__content {
    text-transform: capitalize;
  }
}
</style>
<style lang="scss">
.inverted-list-item {
  color: white !important;
  .v-list-item.v-list-item--active {
    &.theme--light {
      color: map-get($map: $material-dark, $key: background) !important;
    }
    &.theme--dark {
      color: map-get($map: $material-light, $key: background) !important;
    }
  }
}
</style>