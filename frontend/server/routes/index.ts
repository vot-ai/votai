import Router from '@koa/router'
import auth from './authentication'
import user from './user'
import survey from './survey'

const api = new Router()

// Auth routes
api.use('/auth', auth.routes(), auth.allowedMethods())

// User routes
api.use('/user', user.routes(), user.allowedMethods())

// Survey routes
api.use('/survey', survey.routes(), survey.allowedMethods())

export default api
