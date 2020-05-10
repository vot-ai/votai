import { Context, Next } from 'koa'
import consola from 'consola'
import { BaseRequestError } from '../errors'

export const errorMiddleware = () => async (ctx: Context, next: Next) => {
  try {
    await next()
  } catch (err) {
    // Handle error if is a RequestError
    if (err instanceof BaseRequestError) {
      if (err.logToConsole) {
        consola.error(err)
      }
      ctx.status = err.status
      ctx.body = {
        message: err.errorMessage,
        error: err.errorBody
      }
    } else {
      // If it isn't, let Koa's default handler have it
      throw err
    }
  }
}
