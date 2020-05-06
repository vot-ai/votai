/* eslint-disable camelcase */
export enum ResponseStatus {
  VALIDATION_ERROR = 400,
  OK = 200
}

export enum ResponseMessages {
  VALIDATION_ERROR = 'Error validating the request data'
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
}
