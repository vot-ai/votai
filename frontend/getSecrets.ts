import { readFileSync, accessSync, constants } from 'fs'
import { join } from 'path'
import { parse } from 'dotenv'

export default function (moduleOptions: { path: string, filename: string }) {
  const options = {
    path: './',
    filename: 'secrets',
    ...moduleOptions
  }

  const envFilePath = join(options.path, options.filename)

  try {
    accessSync(envFilePath, constants.R_OK)
  } catch (err) {
    return
  }

  return parse(readFileSync(envFilePath))
}
