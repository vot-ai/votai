import Router from '@koa/router'
import { githubAuthMiddleware } from '../middlewares/social'

const facebook = new Router()
const github = new Router()
const social = new Router()
const auth = new Router()

// Social providers
// facebook.post('/', facebookLogin())
github.post('/', githubAuthMiddleware())

// Social endpoints
social.use('/facebook', facebook.routes(), facebook.allowedMethods())
social.use('/github', github.routes(), github.allowedMethods())

// Auth endpoints
auth.use('/social', social.routes(), social.allowedMethods())

export default auth
