import { Context } from '@nuxt/types'

// @ts-ignore
// import colors from 'vuetify/lib/util/colors'

export default function({ app }: Context) {
  return {
    lang: {
      t: (key: string, ...params: any[]) => app.i18n.t(key, params)
    },
    theme: {
      options: {
        customProperties: true
      },
      themes: {
        light: {
          primary: '#000',
          secondary: '#a5a5a5'
        },
        dark: {
          primary: '#fff',
          secondary: '#a5a5a5'
        }
      }
    }
  }
}
