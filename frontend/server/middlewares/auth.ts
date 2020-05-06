/* eslint-disable camelcase */
import { Next, Context } from 'koa'
import compose from 'koa-compose'
import koaJwt from 'koa-jwt'
import jwt from 'jsonwebtoken'
import axios from 'axios'
import { OAuthRequest, OAuthResponse } from '../types/oauth'
import {
  ContextWithState,
  UserState,
  OAuthRequestState,
  OAuthResponseState
} from '../types/context'
import { ResponseStatus, TokenResponse } from '../types/responses'

export const generateJwt = () => (ctx: ContextWithState<UserState>) => {
  const user = ctx.state.user.serialize()

  const token = jwt.sign(user, process.env.JWT_SECRET || 'my_secret', {
    expiresIn: parseInt(process.env.JWT_LIFETIME || '3600')
  })
  const refreshToken = jwt.sign(
    user,
    process.env.JWT_REFRESH_SECRET || 'my_other_secret',
    { expiresIn: parseInt(process.env.JWT_REFRESH_LIFETIME || '86400') }
  )
  const response: TokenResponse = {
    access_token: token,
    refresh_token: refreshToken
  }
  ctx.status = ResponseStatus.OK
  ctx.body = response
}

const validateRefreshToken = () =>
  koaJwt({ secret: process.env.JWT_REFRESH_SECRET || 'my_other_secret' })

export const parseOAuthRequestData = () => async (ctx: Context, next: Next) => {
  const oauthRequest: OAuthRequest = ctx.request.body
  ctx.state.oauthRequest = oauthRequest
  await next()
}

export const getOauthToken = (endpoint: string) => async (
  ctx: ContextWithState<OAuthRequestState>,
  next: Next
) => {
  const oauthRequest = ctx.state.oauthRequest
  const response = await axios.post(endpoint, oauthRequest, {
    headers: { Accept: 'application/json' }
  })
  const responseTokens: OAuthResponse = {
    access_token: response.data.access_token,
    refresh_token: response.data.refresh_token
  }
  ctx.state.oauthResponse = responseTokens
  await next()
}

export const fetchOauthUser = (endpoint: string) => async (
  ctx: ContextWithState<OAuthResponseState>,
  next: Next
) => {
  const responseTokens = ctx.state.oauthResponse
  const response = await axios.get(endpoint, {
    headers: {
      Authorization: `Bearer ${responseTokens.access_token}`,
      Accept: 'application/json'
    }
  })
  ctx.state.rawUserData = response.data
  await next()
}

export const updateTokens = () =>
  compose([validateRefreshToken(), generateJwt()])
