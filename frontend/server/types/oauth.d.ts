/* eslint-disable camelcase */
interface OAuthRequest {
  code: string
  client_id: string
  redirect_uri: string
  response_type: string
  audience?: string
  grant_type?: string
}
