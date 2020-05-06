import mongoose, {
  Document,
  Types,
  Schema,
  DocumentQuery,
  Model
} from 'mongoose'

/**
 * Subdocument containing information about connections (OAuth resources)
 */
const ConnectionSchema: Schema = new Schema({
  provider: { type: String, required: true },
  userId: { type: String, required: true },
  profileData: { type: Object, required: true }
})

/**
 * Actual user schema with basic information about them
 */
const UserSchema: Schema = new Schema(
  {
    // Required attributes
    email: { type: String, required: true, unique: true },
    userId: { type: String, required: true, unique: true },
    name: { type: String, required: true },
    picture: { type: String, required: true },
    // Optional attributes
    givenName: { type: String, required: false },
    familyName: { type: String, required: false },
    // Meta attributes
    identities: [ConnectionSchema]
  },
  { timestamps: true }
)

/**
 * Serialized user connection ready to be transmitted
 */
interface SerializedConnection {
  provider: string
  userId: string
  profileData: { [key: string]: any }
}

/**
 * Connection instance as returned by mongo
 */
interface IConnection extends Types.Subdocument, SerializedConnection {}

/**
 * Serialized user ready to be transmitted
 */
export interface SerializedUser {
  email: string
  userId: string
  name: string
  picture: string
  givenName?: string
  familyName?: string
  identities: SerializedConnection[]
  createdAt: Date
  updatedAt: Date
}

/**
 * Serialize a user
 * @param this Current user instance
 */
const serialize = function(this: IUser) {
  const userObject = this.toObject()
  const serialized: SerializedUser = {
    email: userObject.email,
    userId: userObject.userId,
    name: userObject.name,
    picture: userObject.picture,
    givenName: userObject.givenName,
    familyName: userObject.familyName,
    identities: userObject.identities,
    createdAt: userObject.createdAt,
    updatedAt: userObject.updatedAt
  }
  return serialized
}

/**
 * Query helpers for the user model
 */
const userQueryHelpers = {
  byEmail(this: DocumentQuery<any, IUser>, email: string) {
    return this.findOne({ email })
  }
}

/**
 * User instance as returned by mongo
 */
export interface IUser extends Document, SerializedUser {
  identities: IConnection[]
  serialize: typeof serialize
}

/**
 * Type of the User Model
 */
export interface IUserModel extends Model<IUser, typeof userQueryHelpers> {}

// Register query helpers and methods
UserSchema.query = userQueryHelpers
UserSchema.methods.serialize = serialize

export default mongoose.model<IUser, IUserModel>('User', UserSchema)
