import { Context, DefaultState } from 'koa'
import { IUser } from '../models/user'
import { OAuthRequest, OAuthResponse } from './oauth'

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

export type UserState<S extends DefaultState = DefaultState> = S & {
  user: IUser
}

export type MaybeUserState<S extends DefaultState = DefaultState> = S & {
  user: IUser | null
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
