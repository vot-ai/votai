/* eslint-disable camelcase */
import { Context, Next } from 'koa'
import axios from 'axios'
import jwt from 'jsonwebtoken'
import koaJwt from 'koa-jwt'
import {
  UserData,
  ContextWithState,
  AuthenticatedUserState,
  UnauthenticatedUserState
} from '../types/context'
import UserController from '../controllers/users'
import { OAuthRequest, OAuthResponse } from '../types/oauth'
import {
  TokenResponse,
  ResponseStatus,
  ErrorMessages
} from '../types/responses'
import { IUser, SerializedUser } from '../models/user'
import {
  RequestRegisterdUser,
  RequestUnknownUser,
  RequestAuthenticatedUser,
  RequestAnonUser
} from '../types/requests'
import { Mutable } from '../types/utils'
import { AnonUser } from '../models/anonUser'
import {
  ValidationError,
  ServerError,
  UnauthorizedError,
  BaseRequestError
} from '../errors'

export abstract class BaseAdapter<U> {
  private readonly flowType: 'refresh_token' | 'access_token'
  protected readonly context: Context

  constructor(ctx: Context) {
    this.context = ctx
    const body = ctx.request.body
    if (
      typeof body.refresh_token !== 'undefined' ||
      body.grant_type === 'refresh_token'
    ) {
      this.flowType = 'refresh_token'
    } else {
      this.flowType = 'access_token'
    }
  }

  protected abstract get refreshToken(): string | undefined
  protected abstract accessTokenFlow(): Promise<U>
  protected abstract serializeUser(user: U): string | object | Buffer
  protected abstract deserializeUser(
    serialized: string | object | Buffer
  ): Promise<U>
  protected abstract validateCredentials(): void

  private validateRefreshToken() {
    const refreshToken = this.refreshToken || 'invalid'
    const secret = process.env.JWT_REFRESH_SECRET || 'invalid'
    let parsed
    try {
      parsed = jwt.verify(refreshToken, secret) as string | object | Buffer
    } catch (err) {
      throw new ValidationError(
        ErrorMessages.INVALID_REFRESH_TOKEN,
        err.message
      )
    }
    return parsed
  }

  private async refreshTokenFlow() {
    this.validateCredentials()
    const parsed = this.validateRefreshToken()
    const user = await this.deserializeUser(parsed)
    return user
  }

  generateJWT(user: U) {
    const data = this.serializeUser(user)
    const token = jwt.sign(data, process.env.JWT_SECRET || 'my_secret', {
      expiresIn: parseInt('30')
    })
    const refreshToken = jwt.sign(
      data,
      process.env.JWT_REFRESH_SECRET || 'my_other_secret',
      { expiresIn: parseInt(process.env.JWT_REFRESH_LIFETIME || '86400') }
    )
    const response: TokenResponse = {
      access_token: token,
      refresh_token: refreshToken
    }
    return response
  }

  public async executeFlow() {
    let user: U
    if (this.flowType === 'access_token') {
      user = await this.accessTokenFlow()
    } else {
      user = await this.refreshTokenFlow()
    }
    return this.generateJWT(user)
  }
}

export abstract class BaseOAuthAdapter extends BaseAdapter<IUser> {
  protected readonly oauthRequest: OAuthRequest
  protected readonly tokenType: string = 'Bearer'
  protected readonly clientId: string
  protected readonly clientSecret: string

  // Must be set by derived classes
  protected abstract readonly tokenEndpoint: string
  protected abstract readonly userEndpoint: string

  protected get refreshToken() {
    return this.oauthRequest.refresh_token
  }

  constructor(ctx: Context, clientId: string, clientSecret: string) {
    super(ctx)
    this.clientId = clientId
    this.clientSecret = clientSecret
    this.oauthRequest = ctx.request.body
  }

  protected serializeUser(user: IUser) {
    return user.serialize()
  }

  protected async deserializeUser(serialized: SerializedUser) {
    const user = await UserController.findUserByEmail(serialized)
    if (!user) {
      throw new ValidationError(
        ErrorMessages.USER_NOT_FOUND,
        'Could not find user on the DB'
      )
    }
    return user
  }

  protected async fetchUser(accessToken: string) {
    const response = await axios
      .get(this.userEndpoint, {
        headers: {
          Authorization: `${this.tokenType} ${accessToken}`,
          Accept: 'application/json'
        }
      })
      .catch(e => {
        throw new BaseRequestError(e)
      })
    return response.data
  }

  protected abstract async cleanUser(user: any): Promise<UserData>

  protected async fetchAccessToken() {
    const response = await axios
      .post(this.tokenEndpoint, this.oauthRequest, {
        headers: { Accept: 'application/json' }
      })
      .catch(e => {
        throw new BaseRequestError(e)
      })
    const oauthResponse: OAuthResponse = response.data
    return oauthResponse
  }

  protected async accessTokenFlow() {
    const oauthResponse = await this.fetchAccessToken()
    const rawUser = await this.fetchUser(oauthResponse.access_token)
    const userData = await this.cleanUser(rawUser)
    const user = await UserController.getOrCreateUser(userData)
    if (!user) {
      throw new ServerError(
        ErrorMessages.COULD_NOT_CREATE_USER,
        'Could not create user'
      )
    }
    return user
  }

  protected validateCredentials() {
    const validClientId = this.oauthRequest.client_id === this.clientId
    const validClientSecret =
      this.oauthRequest.client_secret === this.clientSecret
    if (!validClientId || !validClientSecret) {
      throw new UnauthorizedError(
        ErrorMessages.INVALID_CREDENTIALS,
        'Credentials provded are invalid'
      )
    }
  }
}

export class AnonymousAdapter extends BaseAdapter<AnonUser> {
  protected get refreshToken() {
    return this.context.request.body.refresh_token as string | undefined
  }

  protected serializeUser(user: AnonUser) {
    return user.serialize()
  }

  protected deserializeUser(serialized: ReturnType<AnonUser['serialize']>) {
    return Promise.resolve(new AnonUser(serialized.uuid))
  }

  protected validateCredentials() {}

  protected accessTokenFlow() {
    return Promise.resolve(AnonUser.createAnonUser())
  }
}

const baseAuthMiddleware = async <U, T extends BaseAdapter<U>>(
  ctx: ContextWithState<UnauthenticatedUserState>,
  adapter: T
) => {
  const response = await adapter.executeFlow()
  ctx.body = response
  ctx.status = ResponseStatus.OK
}

export const oauthMiddleware = <T extends BaseOAuthAdapter>(
  AdapterClass: new (...args: any[]) => T,
  clientId: string,
  clientSecret: string
) => async (ctx: ContextWithState<UnauthenticatedUserState>) => {
  const adapter = new AdapterClass(ctx, clientId, clientSecret)
  await baseAuthMiddleware(ctx, adapter)
}

export const anonMiddleware = () => async (
  ctx: ContextWithState<UnauthenticatedUserState>
) => {
  const adapter = new AnonymousAdapter(ctx)
  await baseAuthMiddleware(ctx, adapter)
}

/**
 * Authenticates the user and creates the ctx.state.user object
 */
export const authenticationMiddleware = () => async (
  ctx: Context,
  next: Next
) => {
  try {
    await koaJwt({ secret: process.env.JWT_SECRET || 'my_secret' })(ctx, () =>
      Promise.resolve()
    )
    // User is authenticated. Check if the user is registered
    const authCtx = ctx as ContextWithState<AuthenticatedUserState>
    if ('name' in authCtx.state.user) {
      // User is registered. Retrieve IUser from database
      const user = (await UserController.findUserByEmail(
        ctx.state.user
      )) as Mutable<RequestRegisterdUser> | null
      if (!user) {
        // This will be caught by the catch path
        throw new Error('User not on DB')
      }
      user.isRegistered = true
      user.isAuthenticated = true
      authCtx.state.user = user as RequestRegisterdUser
    } else {
      const user = (new AnonUser(
        authCtx.state.user.uuid
      ) as unknown) as Mutable<RequestAnonUser>
      user.isAuthenticated = true
      user.isRegistered = false
      authCtx.state.user = user as RequestAnonUser
    }
  } catch (e) {
    // User is not authenticated
    const authCtx = ctx as ContextWithState<UnauthenticatedUserState>
    authCtx.state.user = { isAuthenticated: false, isRegistered: false }
  }
  await next()
}

export const isAuthenticated = (
  user: RequestUnknownUser
): user is RequestAuthenticatedUser => user.isAuthenticated
export const isRegistered = (
  user: RequestUnknownUser
): user is RequestRegisterdUser => user.isRegistered
