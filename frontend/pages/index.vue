<template>
  <v-layout column justify-center align-center>
    <v-flex xs12 sm8 md6>
      <div class="text-center">
        <logo />
        <vuetify-logo />
      </div>
      <v-card>
        <v-card-title
          class="headline"
        >{{ $t('welcome') }} hey {{ $auth.loggedIn ? $auth.user.email : "anon" }}</v-card-title>
        <v-card-text>
          <p>
            Vuetify is a progressive Material Design component framework for
            Vue.js. It was designed to empower developers to create amazing
            applications.
          </p>
          <p>
            For more information on Vuetify, check out the
            <a
              href="https://vuetifyjs.com"
              target="_blank"
            >documentation</a>.
          </p>
          <p>
            If you have questions, please join the official
            <a
              href="https://chat.vuetifyjs.com/"
              target="_blank"
              title="chat"
            >discord</a>.
          </p>
          <p>
            Find a bug? Report it on the github
            <a
              href="https://github.com/vuetifyjs/vuetify/issues"
              target="_blank"
              title="contribute"
            >issue board</a>.
          </p>
          <p>
            Thank you for developing with Vuetify and I look forward to bringing
            more exciting features in the future.
          </p>
          <div class="text-xs-right">
            <em>
              <small>&mdash; John Leider</small>
            </em>
          </div>
          <hr class="my-3" />
          <a href="https://nuxtjs.org/" target="_blank">Nuxt Documentation</a>
          <br />
          <a href="https://github.com/nuxt/nuxt.js" target="_blank">Nuxt GitHub</a>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" @click="localeChange">Locale</v-btn>
          <v-btn color="primary" @click="$auth.logout()">Logout</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script lang="ts">
import { defineComponent } from 'nuxt-composition-api'
// import { useToast } from 'vue-toastification/composition'

import Logo from '~/components/Logo.vue'
import VuetifyLogo from '~/components/VuetifyLogo.vue'

export default defineComponent({
  ...{ auth: false },
  components: {
    Logo,
    VuetifyLogo
  },
  setup() {},
  mounted() {
    // @ts-ignore
    window.auth = this.$auth
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
