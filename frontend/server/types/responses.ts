/* eslint-disable camelcase */
export enum ResponseStatus {
  VALIDATION_ERROR = 400,
  UNAUTHORIZED_ERROR = 401,
  FORBIDDEN_ERROR = 403,
  NOT_FOUND = 404,
  OK = 200,
  CREATED = 201,
  DELETED = 204,
  SERVER_ERROR = 500
}

export enum ResponseMessages {
  VALIDATION_ERROR = 'Error validating the request data',
  UNAUTHORIZED_ERROR = 'Authorization Error',
  FORBIDDEN_ERROR = "You don't have permission to do that",
  OK = 'Request successful',
  CREATED = 'Resource created',
  DELETED = 'Resource deleted',
  SERVER_ERROR = 'Server error',
  NOT_FOUND = 'Resource not found'
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
}

export enum ErrorMessages {
  INVALID_REFRESH_TOKEN = 'invalid_refresh_token',
  INVALID_PASSWORD = 'invalid_password',
  INVALID_CREDENTIALS = 'invalid_credentials',
  USER_NOT_FOUND = 'user_not_found',
  SURVEY_NOT_FOUND = 'survey_not_found',
  ANNOTATOR_NOT_FOUND = 'annotator_not_found',
  COULD_NOT_CREATE_USER = 'could_not_create_user',
  COULD_NOT_CREATE_SURVEY = 'could_not_create_survey',
  COULD_NOT_UPDATE_SURVEY = 'could_not_update_survey'
}
