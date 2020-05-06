/* eslint-disable camelcase */
export enum ResponseStatus {
  VALIDATION_ERROR = 400,
  UNAUTHORIZED_ERROR = 401,
  FORBIDDEN_ERROR = 403,
  OK = 200
}

export enum ResponseMessages {
  VALIDATION_ERROR = 'Error validating the request data',
  UNAUTHORIZED_ERROR = 'Authentication Error',
  FORBIDDEN_ERROR = "You don't have permission to do that"
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
}
