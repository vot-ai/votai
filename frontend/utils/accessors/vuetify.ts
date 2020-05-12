import { Framework } from 'vuetify'

// eslint-disable-next-line import/no-mutable-exports
let $vuetify: Framework

export function initializeVuetify(vuetify: Framework) {
  $vuetify = vuetify
}

export { $vuetify }
