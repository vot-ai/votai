/* eslint-disable camelcase */
import { Context } from 'koa'
import axios from 'axios'
import jwt from 'jsonwebtoken'
import { UserData } from '../types/context'
import UserController from '../controllers/users'
import { OAuthRequest, OAuthResponse } from '../types/oauth'
import { TokenResponse, ResponseStatus } from '../types/responses'
import { IUser, SerializedUser } from '../models/user'

export const generateJWT = (user: IUser) => {
  const serializedUser = user.serialize()
  const token = jwt.sign(
    serializedUser,
    process.env.JWT_SECRET || 'my_secret',
    {
      expiresIn: parseInt(process.env.JWT_LIFETIME || '3600')
    }
  )
  const refreshToken = jwt.sign(
    serializedUser,
    process.env.JWT_REFRESH_SECRET || 'my_other_secret',
    { expiresIn: parseInt(process.env.JWT_REFRESH_LIFETIME || '86400') }
  )
  const response: TokenResponse = {
    access_token: token,
    refresh_token: refreshToken
  }
  return response
}

export abstract class BaseOAuthAdapter {
  private readonly flowType: 'refresh_token' | 'access_token'
  protected readonly oauthRequest: OAuthRequest
  protected readonly tokenType: string = 'Bearer'
  protected readonly clientId: string
  protected readonly clientSecret: string

  // Must be set by derived classes
  protected abstract readonly tokenEndpoint: string
  protected abstract readonly userEndpoint: string

  constructor(ctx: Context, clientId: string, clientSecret: string) {
    this.clientId = clientId
    this.clientSecret = clientSecret
    this.oauthRequest = ctx.request.body
    if (this.oauthRequest.grant_type === 'refresh_token') {
      this.flowType = 'refresh_token'
    } else {
      this.flowType = 'access_token'
    }
  }

  protected async fetchUser(accessToken: string) {
    const response = await axios.get(this.userEndpoint, {
      headers: {
        Authorization: `${this.tokenType} ${accessToken}`,
        Accept: 'application/json'
      }
    })
    // TODO: Check if fetch user failed here
    return response.data
  }

  protected abstract async cleanUser(user: any): Promise<UserData>

  protected async fetchAccessToken() {
    const response = await axios.post(this.tokenEndpoint, this.oauthRequest, {
      headers: { Accept: 'application/json' }
    })
    // TODO: Check if fetch token failed
    const oauthResponse: OAuthResponse = response.data
    return oauthResponse
  }

  private async accessTokenFlow() {
    const oauthResponse = await this.fetchAccessToken()
    const rawUser = await this.fetchUser(oauthResponse.access_token)
    const userData = await this.cleanUser(rawUser)
    const user = await UserController.getOrCreateUser(userData)
    return user
  }

  protected validateCredentials() {
    const validClientId = this.oauthRequest.client_id === this.clientId
    const validClientSecret =
      this.oauthRequest.client_secret === this.clientSecret
    // TODO: Throw error if invalid
    return validClientId && validClientSecret
  }

  private validateRefreshToken() {
    const refreshToken = this.oauthRequest.refresh_token || 'invalid'
    const secret = process.env.JWT_REFRESH_SECRET || 'invalid'
    // TODO: Handle this error
    const parsed = jwt.verify(refreshToken, secret) as SerializedUser
    return parsed
  }

  private async refreshTokenFlow() {
    this.validateCredentials()
    const parsed = this.validateRefreshToken()
    const user = await UserController.findUserByEmail(parsed)
    return user
  }

  private getJWT(user: IUser) {
    return generateJWT(user)
  }

  public async executeFlow() {
    let user: IUser | null
    if (this.flowType === 'access_token') {
      user = await this.accessTokenFlow()
    } else {
      user = await this.refreshTokenFlow()
    }
    if (user) {
      return this.getJWT(user)
    } else {
      throw new Error('TODO: Write descriptive error message')
    }
  }
}

export const oauthMiddleware = <T extends BaseOAuthAdapter>(
  AdapterClass: new (...args: any[]) => T,
  clientId: string,
  clientSecret: string
) => async (ctx: Context) => {
  const adapter = new AdapterClass(ctx, clientId, clientSecret)
  const response = await adapter.executeFlow()
  ctx.status = ResponseStatus.OK
  ctx.body = response
}
