import { createStorage } from '../localStorage'

const storage = createStorage('auth')

export const getToken = () => storage.read<string>({ key: 'token' })
export const setToken = (token: string) => storage.write({ key: 'token', value: token })
export const removeToken = () => storage.remove({ key: 'token' })

export const getRefreshToken = () => storage.read<string>({ key: 'refresh_token' })
export const setRefreshToken = (token: string) => storage.write({ key: 'refresh_token', value: token })
export const removeRefreshToken = () => storage.remove({ key: 'refresh_token' })

export const getUser = () => storage.read<{ id: string; email: string }>({ key: 'user' })
export const setUser = (user: object) => storage.write({ key: 'user', value: user })
export const removeUser = () => storage.remove({ key: 'user' })

export const clearAuth = () => {
  removeToken()
  removeRefreshToken()
  removeUser()
}
