import { Context, Next } from 'koa'
import jwt from 'jsonwebtoken'
import { ResponseMessages, ResponseStatus } from '../types/responses'

const notEmptyObject = (obj: any): obj is object =>
  obj && obj.constructor === Object && Object.keys(obj).length !== 0

// Middleware that reads encrypted cookies and sets them on state
export const loadApplicationCookies = (path: string = 'user_cache') => async (
  ctx: Context,
  next: Next
) => {
  const emptyCookies = {}
  ctx.state.cookies = emptyCookies
  // First load into state
  const cookieData = ctx.cookies.get(path)
  if (cookieData) {
    try {
      const cookies = jwt.verify(
        cookieData,
        process.env.JWT_SECRET || 'my_secret'
      )
      ctx.state.cookies = cookies
    } catch (e) {}
  }
  await next()
  // Then save modified cookies into header
  const finalCookies = ctx.state.cookies
  if (notEmptyObject(finalCookies)) {
    const hashedCookies = jwt.sign(
      finalCookies,
      process.env.JWT_SECRET || 'my_secret'
    )
    ctx.cookies.set(path, hashedCookies)
  } else {
    // Or remove them if they are not defined
    ctx.cookies.set(path, '')
  }
}

export const clearCookies = () => (ctx: Context) => {
  ctx.state.cookies = undefined
  ctx.body = ResponseMessages.OK
  ctx.status = ResponseStatus.OK
}
