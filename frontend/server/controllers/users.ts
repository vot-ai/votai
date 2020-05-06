import User from '../models/user'
import { UserData } from '../types/context'

class UserController {
  private create = async (userData: UserData) => {
    const { provider, profileData, ...user } = userData
    const newUserBody = {
      ...user,
      identities: [{ provider, userId: user.userId, profileData }]
    }
    return await User.create(newUserBody).catch(() => null)
  }

  public findUserByEmail = async (
    userData: Pick<UserData, 'email'> & Partial<UserData>
  ) => {
    const { email } = userData
    return await User.find()
      .byEmail(email)
      .exec()
  }

  public getOrCreateUser = async (userData: UserData) => {
    const user = await this.findUserByEmail(userData)
    if (user) {
      return user
    } else {
      return await this.create(userData)
    }
  }
}

export default new UserController()
