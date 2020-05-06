/* eslint-disable camelcase */
export interface OAuthRequest {
  code: string
  client_id: string
  client_secret: string
  redirect_uri: string
  response_type: string
  audience?: string
  grant_type?: string
}

export interface OAuthResponse {
  access_token: string
  refresh_token?: string
}
