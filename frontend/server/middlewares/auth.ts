/* eslint-disable camelcase */
import Koa from 'koa'
import compose from 'koa-compose'
import koaJwt from 'koa-jwt'
import jwt from 'jsonwebtoken'
import axios from 'axios'

interface OAuthRequest {
  code: string
  client_id: string
  client_secret: string
  redirect_uri: string
  response_type: string
  audience?: string
  grant_type?: string
}

const generateJwt = () => (ctx: Koa.Context) => {
  const user = ctx.state.user
  const token = jwt.sign(user, process.env.JWT_SECRET || 'my_secret', {
    expiresIn: parseInt(process.env.JWT_LIFETIME || '3600')
  })
  const refreshToken = jwt.sign(
    user,
    process.env.JWT_REFRESH_SECRET || 'my_other_secret',
    { expiresIn: parseInt(process.env.JWT_REFRESH_LIFETIME || '86400') }
  )
  const response = {
    access_token: token,
    refresh_token: refreshToken
  }
  ctx.status = 200
  ctx.body = response
}

const validateRefreshToken = () =>
  koaJwt({ secret: process.env.JWT_REFRESH_SECRET || 'my_other_secret' })

const parseOAuthRequestData = () => async (
  ctx: Koa.Context,
  next: Koa.Next
) => {
  const oauthRequest: OAuthRequest = ctx.request.body
  ctx.state.oauthRequest = oauthRequest
  await next()
}

const getOauthToken = (endpoint: string) => async (
  ctx: Koa.Context,
  next: Koa.Next
) => {
  const oauthRequest: OAuthRequest = ctx.state.oauthRequest
  const response = await axios.post(endpoint, oauthRequest, {
    headers: { Accept: 'application/json' }
  })
  const responseTokens: { access_token?: string; refresh_token?: string } = {
    access_token: response.data.access_token,
    refresh_token: response.data.refresh_token
  }
  ctx.state.oauthResponse = responseTokens
  await next()
}

const fetchOauthUser = (endpoint: string) => async (
  ctx: Koa.Context,
  next: Koa.Next
) => {
  const responseTokens: { access_token?: string; refresh_token?: string } =
    ctx.state.oauthResponse
  const response = await axios.get(endpoint, {
    headers: {
      Authorization: `Bearer ${responseTokens.access_token}`,
      Accept: 'application/json'
    }
  })
  ctx.state.user = response.data
  await next()
}

const getOrCreateUser = () => async (ctx: Koa.Context, next: Koa.Next) => {
  const oauthUser = ctx.state.user
  // Check user and save into database
  ctx.state.user = { id: 123, ...oauthUser }
  await next()
}

const socialLogin = ({
  tokenEndpoint,
  userEndpoint
}: {
  tokenEndpoint: string
  userEndpoint: string
}) =>
  compose([
    parseOAuthRequestData(),
    getOauthToken(tokenEndpoint),
    fetchOauthUser(userEndpoint),
    getOrCreateUser(),
    generateJwt()
  ])

export const githubLogin = () =>
  socialLogin({
    tokenEndpoint: 'https://github.com/login/oauth/access_token',
    userEndpoint: 'https://api.github.com/user'
  })

export const facebookLogin = () =>
  socialLogin({
    tokenEndpoint: 'https://facebook.com/v2.12/dialog/oauth',
    userEndpoint: 'https://graph.facebook.com/v2.12/me?fields=about,name,email'
  })

export const updateTokens = () =>
  compose([validateRefreshToken(), generateJwt()])
