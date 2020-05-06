import { BaseOAuthAdapter, oauthMiddleware } from './auth'

class GithubAdapter extends BaseOAuthAdapter {
  protected readonly tokenEndpoint =
    'https://github.com/login/oauth/access_token'

  protected readonly userEndpoint = 'https://api.github.com/user'

  protected async cleanUser(user: any) {
    const userData = {
      email: user.email,
      userId: user.id.toString(),
      name: user.name,
      picture: user.avatar_url,
      provider: 'github',
      profileData: user,
      familyName: undefined,
      givenName: undefined
    }
    return await userData
  }
}

export const githubAuthMiddleware = () =>
  oauthMiddleware(
    GithubAdapter,
    process.env.GITHUB_CLIENT_ID || 'invalid',
    process.env.GITHUB_CLIENT_SECRET || 'invalid'
  )
