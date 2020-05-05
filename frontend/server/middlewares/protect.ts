import jwt from "koa-jwt"

export default () => jwt({ secret: process.env.JWT_SECRET || 'my_secret' })
