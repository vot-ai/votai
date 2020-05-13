import { Configuration } from '@nuxt/types'
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
  mode: 'spa',
  server: {
    port: 3000,
    host: '0.0.0.0'
  },
  features: {
    transitions: false
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
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      {
        rel: 'stylesheet',
        type: 'text/css',
        href: 'https://cdn.jsdelivr.net/npm/animate.css@3.5.1'
      }
    ]
  },
  /*
   ** Customize the progress-bar color
   */
  loading: { color: '#fff' },
  /*
   ** Global CSS
   */
  css: ['@/assets/scss/fonts.scss', '@/assets/scss/global.scss'],
  /*
   ** Plugins to load before mounting the App
   */
  plugins: [
    { src: '~/plugins/vuex-persist', ssr: false },
    '~/plugins/components',
    '~/plugins/accessors',
    '~/plugins/vue-the-mask'
  ],
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
          logout: { url: '/api/auth/logout', method: 'get' }
        }
      },
      github: {
        responseType: 'code',
        endpoints: {
          token: `${process.env.API_URL}/api/auth/social/github`,
          userInfo: '/api/user/',
          logout: '/api/auth/logout'
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
      { code: 'en', iso: 'en-US', file: 'en.json' },
      { code: 'pt', iso: 'pt-BR', file: 'pt.json' }
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
    customVariables: ['~/assets/scss/variables.scss'],
    optionsPath: '~/vuetify.options.ts',
    defaultAssets: {
      icons: 'fa'
    },
    treeShake: true
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
