import Auth from '@nuxtjs/auth-next/dist/core/auth'

// eslint-disable-next-line import/no-mutable-exports
let $auth: Auth

export function initializeAuth(authInstance: Auth) {
  $auth = authInstance
}

export { $auth }
