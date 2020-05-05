import Router from '@koa/router'
import auth from './authentication'
import user from './user'

const api = new Router()

// Auth routes
api.use('/auth', auth.routes(), auth.allowedMethods())

// User routes
api.use('/user', user.routes(), user.allowedMethods())

export default api
