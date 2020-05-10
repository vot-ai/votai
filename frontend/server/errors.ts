import { ResponseStatus, ResponseMessages } from './types/responses'

export class BaseRequestError extends Error {
  public errorMessage?: string
  public errorBody?: any
  public readonly status: number = ResponseStatus.OK
  public logToConsole: boolean = true

  constructor(error: Error)
  constructor(message?: string, body?: any, status?: number)
  constructor(messageOrError?: string | Error, body?: any, status?: number) {
    super(
      messageOrError instanceof Error ? messageOrError.message : messageOrError
    )
    let message
    if (messageOrError instanceof Error) {
      const error: Error & { status?: number } = messageOrError
      status = error.status
      message = messageOrError.message
    } else {
      message = messageOrError
    }
    this.errorMessage = message
    this.errorBody = body
    this.message = this.errorMessage || this.message
    if (status) {
      this.status = status
    }
    Object.setPrototypeOf(this, BaseRequestError.prototype)
  }
}

export class ValidationError extends BaseRequestError {
  public errorMessage: string = ResponseMessages.VALIDATION_ERROR
  public readonly status = ResponseStatus.VALIDATION_ERROR
  constructor(...args: any[]) {
    super(...args)
    Object.setPrototypeOf(this, ValidationError.prototype)
  }
}

export class UnauthorizedError extends BaseRequestError {
  public errorMessage: string = ResponseMessages.UNAUTHORIZED_ERROR
  public readonly status = ResponseStatus.UNAUTHORIZED_ERROR
  public logToConsole = false
  constructor(...args: any[]) {
    super(...args)
    Object.setPrototypeOf(this, UnauthorizedError.prototype)
  }
}

export class ForbiddenError extends BaseRequestError {
  public errorMessage: string = ResponseMessages.FORBIDDEN_ERROR
  public readonly status = ResponseStatus.FORBIDDEN_ERROR
  constructor(...args: any[]) {
    super(...args)
    Object.setPrototypeOf(this, ForbiddenError.prototype)
  }
}

export class ServerError extends BaseRequestError {
  public errorMessage: string = ResponseMessages.SERVER_ERROR
  public readonly status = ResponseStatus.SERVER_ERROR
  constructor(...args: any[]) {
    super(...args)
    Object.setPrototypeOf(this, ServerError.prototype)
  }
}

export class NotFoundError extends BaseRequestError {
  public errorMessage: string = ResponseMessages.NOT_FOUND
  public readonly status = ResponseStatus.NOT_FOUND
  constructor(...args: any[]) {
    super(...args)
    Object.setPrototypeOf(this, NotFoundError.prototype)
  }
}
