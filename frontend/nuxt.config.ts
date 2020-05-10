import { Configuration } from '@nuxt/types'
// @ts-ignore
import colors from 'vuetify/es5/util/colors'
import getSecrets from './getSecrets'

const socialProviderSecrets = getSecrets({
  path: process.env.SECRETS_PATH || '',
  filename: 'SOCIAL_PROVIDER_SECRETS'
})

const frontendSecrets = getSecrets({
  path: process.env.SECRETS_PATH || '',
  filename: 'FRONTEND_SECRETS'
})

process.env = { ...process.env, ...socialProviderSecrets, ...frontendSecrets }

const config: Configuration = {
  mode: 'universal',
  server: {
    port: 3000,
    host: '0.0.0.0'
  },

  /*
   ** Headers of the page
   */
  head: {
    titleTemplate: '%s - ' + process.env.npm_package_name,
    title: process.env.npm_package_name || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content: process.env.npm_package_description || ''
      }
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }]
  },
  /*
   ** Customize the progress-bar color
   */
  loading: { color: '#fff' },
  /*
   ** Global CSS
   */
  css: [],
  /*
   ** Plugins to load before mounting the App
   */
  // plugins: [{ src: '~/plugins/vuex-persist', ssr: false }],
  /*
   ** Nuxt.js dev-modules
   */
  buildModules: [
    '@nuxt/typescript-build',
    '@nuxtjs/vuetify',
    'nuxt-composition-api'
  ],
  /*
   ** Nuxt.js modules
   */
  modules: [
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    ['@nuxtjs/pwa', { icon: false }],
    'nuxt-i18n',
    '@nuxtjs/auth-next'
  ],
  env: {
    API_URL: process.env.API_URL || '',
    API_URL_BROWSER: process.env.API_URL_BROWSER || ''
  },
  router: {
    middleware: ['auth']
  },
  /*
   ** Auth module configuration
   ** See https://auth.nuxtjs.org/
   */
  auth: {
    strategies: {
      anonymous: {
        scheme: 'refresh',
        token: {
          property: 'access_token',
          maxAge: 1800,
          type: 'Bearer'
        },
        refreshToken: {
          property: 'refresh_token',
          data: 'refresh_token',
          maxAge: 60 * 60 * 24 * 30
        },
        user: {
          property: false,
          autoFetch: true
        },
        endpoints: {
          login: { url: '/api/auth/anon/token', method: 'post' },
          refresh: { url: '/api/auth/anon/token', method: 'post' },
          user: { url: '/api/user', method: 'get' },
          logout: { url: '/api/auth/logout', method: 'post' }
        }
      },
      github: {
        responseType: 'code',
        endpoints: {
          token: `${process.env.API_URL}/api/auth/social/github`,
          userInfo: '/api/user/',
          logout: { url: '/api/auth/logout', method: 'post' }
        },
        clientId: process.env.GITHUB_CLIENT_ID,
        clientSecret: process.env.GITHUB_CLIENT_SECRET
      }
    },
    plugins: ['~/plugins/auth.ts']
  },
  /*
   ** Axios module configuration
   ** See https://axios.nuxtjs.org/options
   */
  axios: {},
  /**
   * i18n module configuration
   * See https://nuxt-community.github.io/nuxt-i18n/
   */
  i18n: {
    lazy: true,
    langDir: 'locales/',
    locales: [
      { code: 'en', iso: 'en-US', file: 'en.ts' },
      { code: 'pt', iso: 'pt-BR', file: 'pt.ts' }
    ],
    strategy: 'no_prefix',
    defaultLocale: 'pt',
    detectBrowserLanguage: {
      alwaysRedirect: true
    },
    vuex: {
      moduleName: 'i18n',
      syncLocale: true,
      syncMessages: false,
      syncRouteParams: true
    },
    vueI18n: {
      fallbackLocale: 'pt'
    }
  },
  /*
   ** vuetify module configuration
   ** https://github.com/nuxt-community/vuetify-module
   */
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: true,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        }
      }
    }
  },
  /*
   ** Build configuration
   */
  build: {
    /*
     ** You can extend webpack config here
     */
    watch: ['types'],
    extend(config, ctx) {
      if (ctx.isDev) {
        config.devtool = ctx.isClient ? 'source-map' : 'inline-source-map'
      }
    }
  },
  typescript: {
    typeCheck: {
      eslint: true
    }
  }
}

export default config
