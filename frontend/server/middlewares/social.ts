/* eslint-disable camelcase */
import { Next } from 'koa'
import compose from 'koa-compose'
import {
  RawUserData,
  UserData,
  ContextWithState,
  RawUserDataState
} from '../types/context'
import UserController from '../controllers/users'
import {
  parseOAuthRequestData,
  getOauthToken,
  fetchOauthUser,
  generateJwt
} from './auth'

type parserFunction = (rawUserData: RawUserData) => UserData | Promise<UserData>

const parseRawUserData = (parser: parserFunction) => async (
  ctx: ContextWithState<RawUserDataState>,
  next: Next
) => {
  const userData = await parser(ctx.state.rawUserData)
  ctx.state.userData = userData
  await next()
}

const socialLogin = ({
  tokenEndpoint,
  userEndpoint,
  parser
}: {
  tokenEndpoint: string
  userEndpoint: string
  parser: parserFunction
}) =>
  compose([
    parseOAuthRequestData(),
    getOauthToken(tokenEndpoint),
    fetchOauthUser(userEndpoint),
    parseRawUserData(parser),
    UserController.setUserByEmail,
    UserController.getOrCreateUser,
    generateJwt()
  ])

interface GithubBaseRawUserData {
  avatar_url: string
  email: string
  id: number
  name: string
}

const githubUserDataParser: parserFunction = (
  rawUserData: GithubBaseRawUserData
) => {
  const userData = {
    email: rawUserData.email,
    userId: rawUserData.id.toString(),
    name: rawUserData.name,
    picture: rawUserData.avatar_url,
    provider: 'github',
    profileData: rawUserData,
    familyName: undefined,
    givenName: undefined
  }
  return userData
}

// const facebookUserDataParser: parserFunction = rawUserData => {
//   return {}
// }

export const githubLogin = () =>
  socialLogin({
    tokenEndpoint: 'https://github.com/login/oauth/access_token',
    userEndpoint: 'https://api.github.com/user',
    parser: githubUserDataParser
  })

// export const facebookLogin = () =>
//   socialLogin({
//     tokenEndpoint: 'https://facebook.com/v2.12/dialog/oauth',
//     userEndpoint: 'https://graph.facebook.com/v2.12/me?fields=about,name,email',
//     parser: facebookUserDataParser
//   })
