import Router from '@koa/router'
import { updateTokens } from '../middlewares/auth'
import { githubLogin } from '../middlewares/social'

const facebook = new Router()
const github = new Router()
const social = new Router()
const token = new Router()
const auth = new Router()

// Social providers
// facebook.post('/', facebookLogin())
github.post('/', githubLogin())

// Social endpoints
social.use('/facebook', facebook.routes(), facebook.allowedMethods())
social.use('/github', github.routes(), github.allowedMethods())

// Token endpoints
token.post('/refresh', updateTokens())

// Auth endpoints
auth.use('/token', token.routes(), token.allowedMethods())
auth.use('/social', social.routes(), social.allowedMethods())

export default auth
