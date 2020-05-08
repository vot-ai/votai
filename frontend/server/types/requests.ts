import { IUser } from '../models/user'
import { AnonUser } from '../models/anonUser'

export type IsAuthenticated = {
  readonly isAuthenticated: true
}

export type IsNotAuthenticated = {
  readonly isAuthenticated: false
}

export type IsRegistered = {
  readonly isRegistered: true
}

export type IsNotRegistered = {
  readonly isRegistered: false
}

export type RequestRegisterdUser = IUser & IsAuthenticated & IsRegistered
export type RequestAnonUser = AnonUser & IsAuthenticated & IsNotRegistered
export type RequestUnauthenticatedUser = IsNotAuthenticated & IsNotRegistered

export type RequestAuthenticatedUser = RequestRegisterdUser | RequestAnonUser
export type RequestUnknownUser =
  | RequestAuthenticatedUser
  | RequestUnauthenticatedUser
