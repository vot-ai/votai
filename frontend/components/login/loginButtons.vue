<template>
  <v-container>
    <v-row class="my-3 text-center">
      <v-col align-self="center">
        <i-btn x-large tile depressed @click="socialLogin('github')">
          <v-icon left>fab fa-github</v-icon>
          {{$t('login.github-button')}}
        </i-btn>
      </v-col>
    </v-row>
    <v-row v-if="!hideAnon" class="text-center">
      <v-col align-self="center">
        <v-btn x-large tile depressed @click="$auth.loginWith('anonymous')">
          <v-icon left>fas fa-user-secret</v-icon>
          {{$t('login.anon-button')}}
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { useContext, defineComponent } from 'nuxt-composition-api'
import { useAuth } from '../../hooks/auth'
export default defineComponent({
  props: {
    hideAnon: Boolean,
    redirect: Boolean
  },
  setup({ redirect }) {
    const auth = useAuth()
    const ctx = useContext()
    const socialLogin = (provider: string) => {
      if (redirect) {
        const from = auth.options.fullPathRedirect
          ? ctx.route.fullPath
          : ctx.route.path
        auth.$storage.setUniversal('redirect', from)
      }
      auth.loginWith(provider)
    }
    return { socialLogin }
  }
})
</script>
