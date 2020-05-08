import { v4 as uuidV4 } from 'uuid'

export class AnonUser {
  public readonly uuid: string
  constructor(uuid: string) {
    this.uuid = uuid
  }

  public serialize() {
    return { uuid: this.uuid }
  }

  static createAnonUser() {
    const uuid = uuidV4()
    return new this(uuid)
  }
}
