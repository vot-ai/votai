import { Context, DefaultState } from 'koa'
import { IUser, SerializedUser } from '../models/user'
import { AnonUser } from '../models/anonUser'
import { OAuthRequest, OAuthResponse } from './oauth'
import {
  RequestAnonUser,
  RequestRegisterdUser,
  RequestUnknownUser,
  RequestUnauthenticatedUser,
  RequestAuthenticatedUser
} from './requests'

/********************************************************************************
 ** Base types
 ********************************************************************************/

export interface UserData {
  email: IUser['email']
  userId: IUser['userId']
  name: IUser['name']
  picture: IUser['picture']
  givenName: IUser['givenName']
  familyName: IUser['familyName']
  provider: IUser['identities'][0]['provider']
  profileData: IUser['identities'][0]['profileData']
}

export type RawUserData = any

/*********************************************************************************
 ** State generics
 *********************************************************************************/

export type UserDataState<S extends DefaultState = DefaultState> = S & {
  userData: UserData
}

export type UnknownUserState<S extends DefaultState = DefaultState> = S & {
  user: RequestUnknownUser
}

export type RegisteredUserState<S extends DefaultState = DefaultState> = S & {
  user: RequestRegisterdUser
}

export type AnonUserState<S extends DefaultState = DefaultState> = S & {
  user: RequestAnonUser
}

export type AuthenticatedUserState<
  S extends DefaultState = DefaultState
> = S & {
  user: RequestAuthenticatedUser
}

export type UnauthenticatedUserState<
  S extends DefaultState = DefaultState
> = S & {
  user: RequestUnauthenticatedUser
}

export type PreAuthenticationUserState<
  S extends DefaultState = DefaultState
> = S & {
  user?: SerializedUser | AnonUser
}

export type RawUserDataState<S extends DefaultState = DefaultState> = S & {
  rawUserData: RawUserData
}

export type OAuthRequestState<S extends DefaultState = DefaultState> = S & {
  oauthRequest: OAuthRequest
}

export type OAuthResponseState<S extends DefaultState = DefaultState> = S & {
  oauthResponse: OAuthResponse
}

/*********************************************************************************
 ** Context generics
 *********************************************************************************/

export interface ContextWithState<S extends DefaultState = DefaultState>
  extends Context {
  state: S
}
