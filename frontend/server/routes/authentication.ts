import { Context } from 'koa'
import Router from '@koa/router'
import { githubAuthMiddleware } from '../middlewares/social'
import { anonMiddleware } from '../middlewares/auth'
import { clearCookies } from '../middlewares/cookies'
import { ResponseMessages, ResponseStatus } from '../types/responses'

const facebook = new Router()
const github = new Router()
const social = new Router()
const anon = new Router()
const auth = new Router()

// Social providers
// facebook.post('/', facebookLogin())
github.post('/', githubAuthMiddleware())

// Social endpoints
social.use('/facebook', facebook.routes(), facebook.allowedMethods())
social.use('/github', github.routes(), github.allowedMethods())

// Anonymous endpoints
anon.post('/token', anonMiddleware())

// Auth endpoints
auth.use('/social', social.routes(), social.allowedMethods())
auth.use('/anon', anon.routes(), anon.allowedMethods())
auth.get('/logout', clearCookies(), (ctx: Context) => {
  if (ctx.query.logout_uri) {
    ctx.redirect(ctx.query.logout_uri)
    return
  }
  ctx.body = ResponseMessages.OK
  ctx.status = ResponseStatus.OK
})

export default auth
